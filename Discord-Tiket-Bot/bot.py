from buttons.controls import *

async def SetupControl():
    channel = client.get_channel(main_Meta["channelSettings"]["tiketControlChannel"])
    count = 0
    async for _ in channel.history(limit=None):
      count += 1
    await channel.purge(limit=count)

    embed = discord.Embed(title="", color=main_Meta["controlEmbedColor"])
    embed.set_image(url=main_Meta["controlHeadImg"])
    await channel.send(embed=embed, view=controlsUI())

@client.event
async def on_ready():
    game = discord.Game(main_Meta["BotActivity"])
    await client.change_presence(status=discord.Status.online, activity=game)
    await client.user.edit(username=main_Meta["BotName"])
    await SetupControl()

client.run(main_Meta["BotToken"])


