from deep_translator import GoogleTranslator
import requests
import wikipedia
import json
import discord
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from nltk.sentiment import SentimentIntensityAnalyzer
from discord import app_commands
from discord.ext import commands
from config import TOKEN, DICT_API_KEY 
from helpers import *
import datetime
import sqlite3
import tabulate


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    """Explanations for when the bot is ready"""
    print("Bot is ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    
@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    """First function created, will be archived"""
    with sqlite3.connect("history.db") as connection:
        cursor = connection.cursor()
        current_time = get_current_time()
        cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?, ?, ?);", ("/hello", interaction.user.mention, current_time))
        connection.commit()
        await interaction.response.send_message(f"Hello {interaction.user.mention}", ephemeral=True)


@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    """Provides a list of commands"""
    with sqlite3.connect("history.db") as connection:
        cursor = connection.cursor()
        current_time = get_current_time()
        cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?, ?, ?);", ("/help", interaction.user.mention, current_time))
        connection.commit()
        await interaction.response.send_message(
            f"""```Hello {interaction.user.name}\n
    The available commands are:\n
    /history <amount>: View the history of commands\n
    /define <word>: Defines a word
    /synonym <word>: Finds synoynms for a word
    /info <topic>: Gives information on a topic from wikipedia
    /translate <passage> <target_language>: Translates a passage into another language
        /classify <word> <context_sentence>: Finds the Part of Speech (type) of a word
    /stem <word>: Finds the stem of a word
    /analyze <sentence>: Provides a sentiment analysis on a passage of text```""", 
    ephemeral=True)

@bot.tree.command(name="history") #make this actually show up...
@app_commands.describe(amount="How many commands do you want to display?")
async def history(interaction: discord.Interaction, amount: int):
    """Displays the history of commands"""
    with sqlite3.connect("history.db") as connection:
        cursor = connection.cursor()
        current_time = get_current_time()
        try:
            history = cursor.execute("SELECT * FROM history ORDER BY datetime DESC LIMIT ?;", (amount,))
            history = history.fetchall()
            history = tabulate.tabulate(history, headers=["Index", "Command", "User", "Timestamp"])
        except Exception as e:
            print(e)
            await interaction.response.send_message(f"The quantity provided was too large.", ephemeral=False)
        cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?, ?, ?);", (f"/history {amount}", interaction.user.mention, current_time))
        connection.commit()
        await interaction.response.send_message(f"{history}", ephemeral=False)

@bot.tree.command(name="define")
@app_commands.describe(word="What word do you want to define?")
async def define(interaction: discord.Interaction, word: str):
    """Defines a word"""
    with sqlite3.connect("history.db") as connection:
        cursor = connection.cursor()
        current_time = get_current_time()
        definition = get_definition(word)
        if definition == -1:
            cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?, ?, ?);", (f"/define {word}", interaction.user.mention, current_time))
            connection.commit()
            await interaction.response.send_message(f"Could not find definition for {word}", ephemeral=False)
        else:
            cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?, ?, ?);", (f"/define {word}", interaction.user.mention, current_time))
            await interaction.response.send_message(f"The definition of {word} is {definition}", ephemeral=False)


@bot.tree.command(name="synonym")
@app_commands.describe(word="What word do you want to find synonyms of?")
async def synonym(interaction: discord.Interaction, word: str):
    """Defines a word"""
    with sqlite3.connect("history.db") as connection:
        cursor = connection.cursor()
        current_time = get_current_time()
        synonyms = get_synonyms(word)
        if synonyms == -1:
            cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?, ?, ?);", (f"/synonym {word}", interaction.user.mention, current_time))
            connection.commit()
            await interaction.response.send_message(f"Could not find synonym(s) for {word}", ephemeral=False)
        else:
            cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?, ?, ?);", (f"/synonym {word}", interaction.user.mention, current_time))
            await interaction.response.send_message(f"Some synonyms of {word} are {synonyms}", ephemeral=False)


@bot.tree.command(name="info")
@app_commands.describe(wikipedia_arg="What do you want information on?")
async def info(interaction: discord.Interaction, wikipedia_arg: str):
    """Gives information of a word from a wikipedia page"""
    with sqlite3.connect("history.db") as connection:
        cursor = connection.cursor()
        current_time = get_current_time()
        try:
            wikipedia_summary = get_info(wikipedia_arg)
            cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?,?,?);", (f"/info {wikipedia_arg}", interaction.user.mention, current_time))
            connection.commit()
            await interaction.response.send_message(f"{wikipedia_summary}", ephemeral=False)
        except Exception as e:
            print(e)
            cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?,?,?);", (f"/info {wikipedia_arg}", interaction.user.mention, current_time))
            connection.commit()
            await interaction.response.send_message(f"{wikipedia_arg} is not available on wikipedia, try being more specific", ephemeral=False)

@bot.tree.command(name="translate")
@app_commands.describe(translate_arg="What should I translate?", target_lang="What language should I translate to?")
async def translate(interaction: discord.Interaction, translate_arg: str, target_lang: str):
    """Translates text into another language"""
    #Creates a dictionary of the most common languages to convert to codes
    with sqlite3.connect("history.db") as connection:
        cursor = connection.cursor()
        current_time = get_current_time()
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(translate_arg)
        cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?, ?, ?);", (f"/translate {translate_arg} {target_lang}", interaction.user.mention, current_time))
        connection.commit()
        await interaction.response.send_message(f"{translated_text}", ephemeral=False)



@bot.tree.command(name="classify")
@app_commands.describe(word="What is the word you want to classify?", sentence = "Give an exaple of a usage of that word")
async def classify(interaction: discord.Interaction, word: str, sentence: str):
    """Returns the Part of Speech of a word (eg. noun, posessive pronoun)"""
    with sqlite3.connect("history.db") as connection:
        cursor = connection.cursor()
        current_time = get_current_time()
        word = word.lower()
        sentence = sentence.lower()
        stop_words = set(stopwords.words('english'))
        tokenized = sent_tokenize(sentence)
        for token in tokenized:
            wordsList = nltk.word_tokenize(token)
            wordsList = [w for w in wordsList if w not in stop_words]
            tagged = nltk.pos_tag(wordsList)
        
            print(tagged)
        for w in range(len(tagged)):
            if tagged[w][0] == word:
                pos_acronym = tagged[w][1]
                pos_word = get_pos_word(pos_acronym)
                cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?, ?, ?);", (f"/classify {word} {sentence}", interaction.user.mention, current_time))
                connection.commit()
                await interaction.response.send_message(f"{word.capitalize()} is a {pos_word.lower()}")
                return
        await interaction.response.send_message("Sorry, I can't classify that word.")



@bot.tree.command(name="stem")
@app_commands.describe(word="What is the word you want to find the stem of?")
async def stem(interaction: discord.Interaction, word: str):
    """Returns the stem of a word (eg. Eating -> Eat)"""
    with sqlite3.connect("history.db") as connection:
        cursor = connection.cursor()
        current_time = get_current_time()
        word = word.lower()
        stemmer = PorterStemmer()
        try:
            stem = stemmer.stem(word)
            cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?, ?, ?);", (f"/stem {word}", interaction.user.mention, current_time))
            connection.commit()
            await interaction.response.send_message(f"The stem of {word.capitalize()} is {stem.capitalize()}")
        except Exception as e:
            cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?, ?, ?);", (f"/stem {word}", interaction.user.mention, current_time))
            connection.commit()
            await interaction.response.send_message(f"Sorry, I can't find the stem of {word.capitalize()}.")

@bot.tree.command(name="analyze")
@app_commands.describe(sentence="What is the sentence you want to analyze?")
async def analyze(interaction: discord.Interaction, sentence: str):
    """Performs sentiment analysis on a piece of text"""
    with sqlite3.connect("history.db") as connection:
        cursor = connection.cursor()
        current_time = get_current_time()
        sia = SentimentIntensityAnalyzer()
        score = sia.polarity_scores(sentence)
        score = score['compound']
        result = ""
        if score < 0:
            if score < -0.5:
                result = "negative"
            else:
                result = "negative-leaning"
        elif score >= 0:
            if score > 0.5:
                result = "positive"
            else:
                result = "positive-leaning"
        cursor.execute("INSERT INTO history (command, user, datetime) VALUES(?, ?, ?);", (f"/analyze {sentence}", interaction.user.mention, current_time))
        connection.commit()
        if result != "":
            await interaction.response.send_message(f"The sentiment of that sentence is {result}")
        else:
            await interaction.response.send_message(f"The sentiment of that sentence is unknown.")

bot.run(TOKEN)
