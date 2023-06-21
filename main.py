from deep_translator import GoogleTranslator
import requests
import wikipedia
import json
import discord
from discord import app_commands
from discord.ext import commands
from config import TOKEN, DICT_API_KEY 
from helpers import *
import datetime
import sqlite3

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
            /command1: definition\n
            /command2: definiton```""", 
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
        except Exception as e:
            print(e)
            await interaction.response.send_message(f"Could not retrieve history. Decrease the limit.", ephemeral=False)
        history = history.fetchall()
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



bot.run(TOKEN)
