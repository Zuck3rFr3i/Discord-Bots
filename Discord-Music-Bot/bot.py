import discord
from discord.ext import commands
from discord import app_commands

from classes.buttons.managebuttons import *

@tasks.loop(minutes=2)
async def checkinactive():
    if len(songqueue) < 1:
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=client.get_guild(main_config["core"]["guildid"]))
        if voice_client:
            if not voice_client.is_playing():
                await voice_client.disconnect()

@tasks.loop(count=1)
async def setupbuttons():
    channel = client.get_channel(main_config["channels"]["botfuncs"])
    count = 0
    async for _ in channel.history(limit=None):
      count += 1
    await channel.purge(limit=count)
    embed = discord.Embed(title="", color=discord.Color.blue())
    embed.set_image(url="BANNER.COM") #Your Banner
    await channel.send(embed=embed, view=musicbuttons(client))

@client.event
async def on_ready():
    await client.user.edit(username=main_config["core"]["botname"])
    checkqueue.start()
    checkinactive.start()
    setupbuttons.start()
    changeactive.start()


client.run(main_config["core"]["bottoken"])