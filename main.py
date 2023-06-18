from deep_translator import GoogleTranslator
import requests
import wikipedia
import json
import discord
from discord import app_commands
from discord.ext import commands
from config import TOKEN, DICT_API_KEY 
from language_codes import LANGUAGE_CODES

#name it lex?

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


def get_definition(word):
    """Accesses the Marriam webster API to get the definition of a word"""
    base_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
    api_key = "?key=" + DICT_API_KEY
	
    print(api_key)
    
    full_api_url = base_url + word + api_key

    try:
        response = requests.get(full_api_url)
        data = json.loads(response.content.decode('utf-8'))[0]
        print(data)
        #Dig through the JSON response to find relevant info
        definition = data['shortdef'][0]
        #Remove text modifiers from raw sentence string
        #print(definition)
        return definition
    except Exception as e:
        print(e)
        return -1

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
    await interaction.response.send_message(f"Hello {interaction.user.mention}", ephemeral=True)


@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    """Provides a list of commands"""
    await interaction.response.send_message(f"```Hello {interaction.user.name}\nThe available commands are:\n/command1: definition\n/command2: definiton```", ephemeral=True)

@bot.tree.command(name="define")
@app_commands.describe(word="What word do you want to define?")
async def define(interaction: discord.Interaction, word: str):
    """Defines a word"""
    definition = get_definition(word)
    if definition == -1:
            await interaction.response.send_message(f"Could not find definition for {word}", ephemeral=False)
    await interaction.response.send_message(f"The definition of {word} is {definition}", ephemeral=False)


@bot.tree.command(name="info")
@app_commands.describe(wikipedia_arg="What do you want information on?")
async def info(interaction: discord.Interaction, wikipedia_arg: str):
    """Gives information of a word from a wikipedia page"""
    try:
        wikipedia_summary = wikipedia.summary(wikipedia_arg, sentences=5, auto_suggest=True, redirect=True)
        await interaction.response.send_message(f"{wikipedia_summary}", ephemeral=False)
    except Exception as e:
        print(e)
        await interaction.response.send_message(f"{wikipedia_arg} is not available on wikipedia", ephemeral=False)

@bot.tree.command(name="translate")
@app_commands.describe(translate_arg="What should I translate?", target_lang="What language should I translate to?")
async def translate(interaction: discord.Interaction, translate_arg: str, target_lang: str):
    """Translates text into another language"""
    #Creates a dictionary of the most common languages to convert to codes
    translated_text = GoogleTranslator(source='auto', target=target_lang).translate(translate_arg)
    await interaction.response.send_message(f"{translated_text}", ephemeral=False)

bot.run(TOKEN)
