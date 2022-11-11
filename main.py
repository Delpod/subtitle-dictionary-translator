import sqlite3
import re
import requests
from tkinter import *
from tkinter import ttk

from config import source_language, target_language, subtitle_file, authorization_key

con = sqlite3.connect('dictionary.db')
cur = con.cursor()

res = cur.execute('SELECT name FROM sqlite_master WHERE type=\'table\' and name=\'known_words\'')
if res.fetchone() is None:
    cur.execute('CREATE TABLE known_words(word text NOT NULL UNIQUE, translation text NOT NULL, PRIMARY KEY("word"))')

res = cur.execute('SELECT name FROM sqlite_master WHERE type=\'table\' and name=\'unknown_words\'')
if res.fetchone() is None:
    cur.execute('CREATE TABLE unknown_words(word text NOT NULL UNIQUE, translation text NOT NULL, PRIMARY KEY("word"))')

window = Tk()
window.geometry("400x500")
window.title("Subitle Dictionary Translator")

label = Label(window, text="Select words below:", font=("Times New Roman", 10), padx=10, pady=10)
label.pack()
listbox = Listbox(window, selectmode="multiple")
yscrollbar = Scrollbar(listbox, command=listbox.yview)
yscrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(padx=10, pady=10, expand=YES, fill="both")

wordlist: set = None
file_read = None
translate_dict = None
translate_wordlist = None

def translate():
    global file_read
    global wordlist
    global translate_dict
    global translate_wordlist

    with open(subtitle_file) as sub_file:
        file_read = sub_file.read()
        wordlist = set([re.sub(r'[\d\W]+$', '', re.sub(r'^[\d\W]+', '', w)).lower() for w in file_read.split()])
        wordlist.remove('')

    cur.execute(f'SELECT word from known_words')
    known_words = cur.fetchall()
    known_words = set([w[0] for w in known_words])

    for w in known_words:
        if w in wordlist:
            wordlist.remove(w)

    words = ','.join(["'" + w.replace("'","''") + "'" for w in wordlist])

    cur.execute(f'SELECT word, translation from unknown_words WHERE word IN ({words})')
    unknown_words = cur.fetchall()
    unknown_words_words = [ w[0] for w in unknown_words ]
    translate_dict = { w[0] : w[1] for w in unknown_words }

    translate_wordlist = [w for w in wordlist if w not in unknown_words_words]

    if len(translate_wordlist) > 0:
        translate_wordlist_joined = '. '.join(translate_wordlist)

        headers = {'Authorization': authorization_key}
        params = {'text': translate_wordlist_joined, 'source_lang': source_language, 'target_lang': target_language }
        r = requests.post('https://api-free.deepl.com/v2/translate', headers=headers, params=params)

        values = r.json()
        print(translate_wordlist_joined)
        print(values)
        translated_words: str = values.get('translations')[0].get('text')
        translated_words = translated_words.rstrip('.').split('. ')
        
        for i, w in enumerate(translate_wordlist):
            translate_dict[w] = translated_words[i]

    for w in sorted(list(wordlist)):
        listbox.insert(END, f'{w} ({translate_dict[w]})')

def save_words():
    global file_read
    global translate_dict
    global translate_wordlist

    translated_words = [translate_dict[w] for w in translate_wordlist]

    cur.executemany(f'INSERT into unknown_words VALUES (?, ?)', zip(translate_wordlist, translated_words))
    con.commit()

def set_as_known():
    global wordlist
    selection: tuple = reversed(listbox.curselection())
    words = sorted(list(wordlist))
    for i in selection:
        w = words[i]
        cur.execute(f'INSERT into known_words VALUES (?, ?)', (w, translate_dict[w]))
        cur.execute(f'DELETE FROM unknown_words WHERE word = \'' + w.replace('\'', '\'\'') + '\'')
        wordlist.remove(w)
        listbox.delete(i)
    con.commit()

def save_file():
    global file_read
    global wordlist
    global translate_dict
    global subtitle_file

    copy_file = file_read
    for i, w in enumerate(wordlist):
        copy_file = re.sub(re.compile('(?<=[^a-zA-Z])' + w + '(?=[^a-zA-Z])'), f'{w} <font color="#ffff99">({translate_dict[w]})</font>', copy_file)

    f = open(f'translated_{subtitle_file}', 'w')
    f.write(copy_file)
    f.close()

def close():
    con.close()
    window.destroy()

translate()
save_words()

btn1 = Button(window, text="Set as known", command=set_as_known)
btn1.pack(padx=10, pady=10, expand=NO, fill=X)
btn2 = Button(window, text="Save file", command=save_file)
btn2.pack(padx=10, pady=10, expand=NO, fill=X)
btn3 = Button(window, text="Quit", command=close)
btn3.pack(padx=10, pady=10, expand=NO, fill=X)

window.mainloop()
