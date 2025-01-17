import os
from email.policy import default

import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name='ping')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

bot.run(TOKEN)