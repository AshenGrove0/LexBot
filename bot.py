import asyncio
import discord
from discord import app_commands
import discord.ext
from discord.ext import commands
import responses
from discord.ext.commands import Bot
import json

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():

    with open('secrets.json', 'r') as f:
        data = json.load(f)
        data = dict(data)
        TOKEN = data["token"]
        SERVER_ID = data["server_id"]
    intents = discord.Intents.all()
    intents.message_content = True
    client = discord.Client(intents=intents)
    tree = discord.app_commands.CommandTree(client)
    

    # sync the slash command to your server
    @client.event
    async def on_ready():
        await tree.sync(guild=discord.Object(id=SERVER_ID))
        # print "ready" in the console when the bot is ready to work
        print("Ready")

    @tree.command(name="name", description="description")
    async def slash_command(interaction: discord.Interaction):    
        await interaction.response.send_message("command")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)