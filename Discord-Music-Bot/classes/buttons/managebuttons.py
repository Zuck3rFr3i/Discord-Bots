from classes.ytdlsource import *
from classes.uis.addsong import *
from discord.ext import tasks

showingqueue = 0
songname = ""

@tasks.loop(seconds=5)
async def changeactive():
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=client.get_guild(main_config["core"]["guildid"]))
    if voice_client:
        if voice_client.is_playing():
            global showingqueue
            if showingqueue == 0:
                game = discord.Game(f"Warteschlange: {len(songqueue)}")
                await client.change_presence(status=discord.Status.online, activity=game)
                showingqueue = 1
            else:
                game = discord.Game(f" {songname}")
                await client.change_presence(status=discord.Status.online, activity=game)
                showingqueue = 0
    else:
        game = discord.Game(f"Wartet auf eine Party.")
        await client.change_presence(status=discord.Status.online, activity=game)

@tasks.loop(seconds=10)
async def checkqueue():
    if len(songqueue) > 0:
        global songname
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=client.get_guild(main_config["core"]["guildid"]))
        if voice_client:
            if not voice_client.is_playing():
                player = await YTDLSource.from_url(songqueue[0], loop=client.loop, stream=True)
                songname = player.data["title"]
                voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                songqueue.pop(0)

class musicbuttons(discord.ui.View):
    def __init__(self, client, timeout=None):
        super().__init__(timeout=timeout)
      
    @discord.ui.button(label="Channel Joinen", style=discord.ButtonStyle.blurple, emoji="✅", row=0)
    async def b1(self, interaction:discord.Interaction, button:discord.Button):        
        voice_client = interaction.guild.voice_client
        if not interaction.user.voice:
            await interaction.response.send_message("Du bist in keinem Voice Channel!", ephemeral=True)
            return
        elif voice_client:
            await interaction.response.send_message("Ich bin bereits in einem Channel!", ephemeral=True)
        elif not voice_client:
            channel = interaction.user.voice.channel
            await channel.connect()
            await interaction.response.defer()

    @discord.ui.button(label="Channel Verlassen", style=discord.ButtonStyle.blurple, emoji="❌", row=0)
    async def b2(self, interaction:discord.Interaction, button:discord.Button):        
        voice_client = interaction.guild.voice_client
        if voice_client:
            await voice_client.disconnect()
            await interaction.response.defer()
        else:
            await interaction.response.send_message("Der bot ist in keinem Channel Connected!", ephemeral=True)

    @discord.ui.button(label="Lied hinzufügen", style=discord.ButtonStyle.green, emoji="➕", row=1)
    async def b3(self, interaction:discord.Interaction, button:discord.Button):
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=client.get_guild(main_config["core"]["guildid"]))
        if voice_client:
            await interaction.response.send_modal(addsong())
        else:
            await interaction.response.send_message("Ich bin in keinem Channel!", ephemeral=True)


    @discord.ui.button(label="Warteschlange Leeren", style=discord.ButtonStyle.red, emoji="✖️", row=1)
    async def b4(self, interaction:discord.Interaction, button:discord.Button):        
        if len(songqueue) > 0:
            songqueue.clear()
            await interaction.response.send_message("Warteschleife wurde bereinigt.", ephemeral=True)
        else:
            await interaction.response.send_message("Ich habe keine Lieder in der Warteschleife!", ephemeral=True)

    @discord.ui.button(label="Aktueller Song", style=discord.ButtonStyle.gray, emoji="❔", row=1)
    async def b9(self, interaction:discord.Interaction, button:discord.Button):
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=client.get_guild(main_config["core"]["guildid"]))
        if voice_client:     
            if voice_client.is_playing():   
                await interaction.response.send_message(f"Aktueller Song: {songname}", ephemeral=True)
            else:
                await interaction.response.defer()
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Abspielen", style=discord.ButtonStyle.green, emoji="▶️", row=2)
    async def b5(self, interaction:discord.Interaction, button:discord.Button):        
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=client.get_guild(main_config["core"]["guildid"]))
        if voice_client:
            if voice_client.is_paused():
                voice_client.resume()
                await interaction.response.defer()
            else:
                await interaction.response.send_message("Ich Spiele grade kein lied ab! Füge eins der Liste hinzu.", ephemeral=True)
        else:
            await interaction.response.send_message("Ich bin in keinem Channel!", ephemeral=True)


    @discord.ui.button(label="Pausieren", style=discord.ButtonStyle.green, emoji="⏸", row=2)
    async def b6(self, interaction:discord.Interaction, button:discord.Button):        
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=client.get_guild(main_config["core"]["guildid"]))
        if voice_client:
            if voice_client.is_playing():
                voice_client.pause()
                await interaction.response.defer()
            else:
                await interaction.response.send_message("Ich Spiele grade kein lied ab! Füge eins der Liste hinzu.", ephemeral=True)
        else:
            await interaction.response.send_message("Ich bin in keinem Channel!", ephemeral=True)

    @discord.ui.button(label="Stoppen", style=discord.ButtonStyle.green, emoji="⏹", row=2)
    async def b8(self, interaction:discord.Interaction, button:discord.Button):        
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=client.get_guild(main_config["core"]["guildid"]))
        if voice_client:
            if voice_client.is_playing():
                voice_client.stop()
                await interaction.response.defer()
            else:
                await interaction.response.send_message("Ich Spiele grade kein lied ab! Füge eins der Liste hinzu.", ephemeral=True)
        else:
            await interaction.response.send_message("Ich bin in keinem Channel!", ephemeral=True)

    @discord.ui.button(label="Nächstes Lied", style=discord.ButtonStyle.green, emoji="⏩", row=2)
    async def b7(self, interaction:discord.Interaction, button:discord.Button):        
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=client.get_guild(main_config["core"]["guildid"]))
        if voice_client:
            if voice_client.is_playing():
                if len(songqueue) > 0:
                    voice_client.stop()
                    await checkqueue()
                    await interaction.response.defer()
                else:
                    await interaction.response.send_message("Die warteschlange ist Leer!", ephemeral=True)
            else:
                await interaction.response.send_message("Ich spiele kein lied.", ephemeral=True)
        else:
            await interaction.response.send_message("Ich bin in keinem Channel!", ephemeral=True)

        


      