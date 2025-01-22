import json
import os
from pprint import pprint

import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from fflogs.characterInfo import get_character

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

with open("resources/serverSlugs.json", "r") as file:
    serverList = json.load(file)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def server_autocomplete(interaction: discord.Interaction, current: str):
    return [app_commands.Choice(name=server, value=server)
            for server in serverList if current.lower() in server.lower()][:25]


@bot.tree.command(name='character', description='Search for a character on FFLogs')
@app_commands.autocomplete(server=server_autocomplete)
async def character(interaction: discord.Interaction, name: str, server: str):
    #await interaction.response.defer(thinking=True)
    #await interaction.response.send_message("Fetching character data, please wait...")
    characterInfo = get_character(name, server)
    if not characterInfo:
        await interaction.followup.send(f"Character `{name}` on `{server}` not found.", ephemeral=True)
        return

    pprint(characterInfo)
    embed = discord.Embed(
        title=characterInfo['name'],
        description=f"Server: {server}",
        color=discord.Color.green(),
        url=f'https://www.fflogs.com/character/id/{characterInfo['id']}'
    )

    embed.set_thumbnail(url=characterInfo['thumbnail'])

    embed.add_field(name="Best Perf. Average", value=f"{characterInfo['overall']['bestPerformanceAverage']:.2f}",
                    inline=True)
    embed.add_field(name="Median Performance Average",
                    value=f"{characterInfo['overall']['medianPerformanceAverage']:.2f}", inline=True)

    embed.add_field(
        name=characterInfo['overall']['zoneName'],
        value="```" +
              f"{'Boss':<18}{'Spec':<8}{'Rank %':<8}{'Kills':<6}{'Rank':<6}\n" +
              "\n".join(
                  f"{parse['bossName']:<18}{parse['bestSpec']:<8}{parse['rankPercent']:<8.2f}{parse['totalKills']:<6}{parse['rank']:<6}"
                  for parse in characterInfo['parses']) +
              "```",
        inline=False
    )

    await  interaction.response.send_message(embed=embed)



bot.run(TOKEN)