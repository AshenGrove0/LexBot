# Lexbot

## Overview
Lexbot is a discord bot with a variety of functions for analysing words and passages of text.


<ALREADY WRITTEN SUMMARY>
  
#### Video Demo: https://youtu.be/kU1z_ugIexw

## Features:

### Commands:
- `/history <amount>`: Provides a list of the previous commands
- `/define <word>`: Defines a word using the Merriam-Webster Dictionary API
- `/synonym <word>`: Finds synoynms for a word using the Merriam-Webster Dictionary API
- `/info <topic>`: Provides information on a topic from wikipedia
- `/translate <passage> <target_language>`: Translates a passage into another language
- `/classify <word> <context_sentence>`: Finds the Part of Speech (type) of a word using the Natural Language Toolkit (NTLK)
- /`stem <word>`: Finds the stem of a word
- `/analyze <sentence>`: Provides a sentiment analysis on a passage of text

### Files:
- `main.py` - Contains all commands and logic for running the bot
- `helpers.py` - Contains helper commands, such as those for API calls, to improve overall readability
- `history.db` - A database with a history of commands, for both users and debugging purposes
- `requirements.txt` - A list of requirements


## Requirements:

### Python Packages:

- [discord](https://pypi.org/project/discord.py/)  
- [deep_translator](https://pypi.org/project/deep-translator/)  
- [requests](https://pypi.org/project/requests/)  
- [wikipedia](https://pypi.org/project/wikipedia/)
- [tabulate](https://pypi.org/project/tabulate/)
- [nltk](https://pypi.org/project/nltk/)

### NTLK Corpora:

- [stopwords](https://www.nltk.org/data.html)

### API Keys/Tokens:

- Merriam-Webster Dictionary
- Merriam-Webster Thesaurus
- Discord Bot Token