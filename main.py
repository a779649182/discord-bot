import os
from email.policy import default

import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View

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

@bot.tree.command(name='character', description='Search for a character on FFLogs')
async def character(interaction: discord.Interaction, name: str, server: str):
    #await interaction.response.send_message("Fetching character data, please wait...")
    embed = discord.Embed(
        title=f"Character Search: {name}",
        description=f"Server: {server}",
        color=discord.Color.green()
    )
    #embed.set_thumbnail(url="https://preview.redd.it/daily-character-discussion-kita-ikuyo-v0-alckatsavcia1.png?width=736&format=png&auto=webp&s=3965d7e5b686028b7e5659fc5aa3195fcfbb3628")

    # Create buttons
    button1 = Button(label="Select Content Type", style=discord.ButtonStyle.primary, custom_id="content_type")
    button2 = Button(label="Filter by Job", style=discord.ButtonStyle.secondary, custom_id="filter_job")

    # Add buttons to a view
    view = View()
    view.add_item(button1)
    view.add_item(button2)

    # Send the embed with the buttons
    await  interaction.response.send_message(embed=embed, view=view)
    #await interaction.edit_original_response(content=None,embed=embed, view=view)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        custom_id = interaction.data.get("custom_id")
        if custom_id == "content_type":
            await interaction.response.send_message("Please select a content type: Raid, Ultimate, etc.")
        elif custom_id == "filter_job":
            await interaction.response.send_message("Please specify a job to filter by.")

bot.run(TOKEN)