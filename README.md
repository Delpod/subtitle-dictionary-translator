# subtitle-dictionary-translator

This is a tool that allows you to translate single words in subtitles (probably in `.srt` or `.txt` format) to any language. The tool uses sqlite and save the words you already know, so in the next runs you won't have to select the worlds you already know. So it takes less and less time.

As it's still work in progress the code is messy, there might be a lot of bugs, it wasn't thoroughly tested. Currently the source language can only be english and target language was only tested with polish.

## Setup

1. Clone the repository
2. Execute `pip install -r requirements.txt`
3. Create DeepL account and get an API Key

  ```Note: this should also work with Google Translate API but would require some changes in code```
  
3. Copy `.env.example` file and rename the copy to `.env`
4. Change values in `.env`, especially add `AUTHORIZATION_KEY` from DeepL account
5. For the first run change `FIRST_RUN=NO` to `FIRST_RUN=YES`

## Using

1. Run with `python main.py`
2. Change frequent words to your liking, default is that 1000 most frequent words are not included in a view
3. Select words you know, and click `Set as known`
4. Click `Save file` if you want to create new subtitles file with the translations included
5. Click `Export words to csv` if you want to learn words at first. This can be imported by any spreadsheet tool

## Future plans

* Cleanup code
* Make it work for different languages
* Save settings
* Add dialog where to save translated file
* Add dialog to pick a file to translate
* Make it possible to switch to Google Translate API
* ... and more
