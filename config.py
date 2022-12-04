import os
from dotenv import load_dotenv

load_dotenv()

source_language = os.getenv('SOURCE_LANGUAGE')
target_language = os.getenv('TARGET_LANGUAGE')
subtitles_file = os.getenv('SUBTITLES_FILE')
frequent_words_file = os.getenv('FREQUENT_WORDS_FILE')
authorization_key = os.getenv('AUTHORIZATION_KEY')
first_run = os.getenv('FIRST_RUN') == 'YES'