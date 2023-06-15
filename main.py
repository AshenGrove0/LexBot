import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import json
from config import TOKEN
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
print(TOKEN)
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

bot.run(TOKEN)