# Lexbot

## Overview
Lexbot is a discord bot with a variety of functions for analysing words and passages of text.


<ALREADY WRITTEN SUMMARY>
  
#### Video Demo: https://youtu.be/kU1z_ugIexw

## Features:

### Commands:
- `/history <amount>`: Provides a list of the previous commands using SQLite3
- `/define <word>`: Defines a word using the Merriam-Webster Dictionary API
- `/synonym <word>`: Finds synoynms for a word using the Merriam-Webster Dictionary API
- `/info <topic>`: Provides information on a topic from wikipedia
- `/translate <passage> <target_language>`: Translates a passage into another language using Google Translate
- `/classify <word> <context_sentence>`: Finds the Part of Speech (type) of a word using the Natural Language Toolkit (NTLK)
- /`stem <word>`: Finds the stem of a word
- `/analyze <sentence>`: Provides a sentiment analysis on a passage of text

### Files:
- `main.py` - Contains all commands and logic for running the bot
- `helpers.py` - Contains helper commands, such as those for API calls, to improve overall readability
- `history.db` - A database with a history of commands, for both users and debugging purposes. This can be viewed within discord with the command `/history <amount>`
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

## Decision Reasoning:

I chose to use Discord as a platform as it removed the need for manually creating a front end - an area a am not particularly interested in - and provided an effective user interface through its chat platform. Bots are also an invaluable part of the ecosystem, incorporated into the vast majority of servers, which means it is easy to be used by others without significant friction.

I chose to use the Merriam-Webster APIs for some functions as they allowed me to practice using the requests library and reduced the amount of menial work that would have been required from implementing my own dictionary, which would have required unnecessary extra scripts. They are also free, which meant there was no up-front cost which would have led it to being a risky choice.