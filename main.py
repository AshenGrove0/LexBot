import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import json
from config import TOKEN
import translate
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
@bot.event
async def on_ready():
    print("Bot is ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    
@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}", ephemeral=True)


@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f"```Hello {interaction.user.name}\nThe available commands are:\n/command1: definition\n/command2: definiton```", ephemeral=True)


@bot.tree.command(name="say")
@app_commands.describe(thing_to_say="What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`", ephemeral=False)

@bot.tree.command(name="translate")
@app_commands.describe(translate_arg="What should I translate?", language="What language should I translate to?")
async def say(interaction: discord.Interaction, translate_arg: str, language: str):
    #Creates a dictionary of the most common languages to convert to codes
    lang_dict = {
        "english": "en",
        "french": "fr",
        "german": "de",
        "spanish": "es",
        "italian": "it",
        "japanese": "ja",
        "korean": "ko",
        "dutch": "nl",
        "polish": "pl",
        "portuguese": "pt",
        "russian": "ru",
        "turkish": "tr",
        "chinese": "zh-CN",
        "chinese Traditional": "zh-TW",
        "chinese Simplified": "zh-CN",
    }
    
    try:
        # Converts the language to a usable language code
        if language.lower() in lang_dict:
            language = lang_dict[language.lower()]
        translator = translate.Translator(language)
        translated_word = translator.translate(translate_arg)
        await interaction.response.send_message(f"{translated_word}", ephemeral=False)
    except Exception as e:
            await interaction.response.send_message(f"Sorry, I don't know that language", ephemeral=False)

bot.run(TOKEN)