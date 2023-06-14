import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import json

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is ready")
        