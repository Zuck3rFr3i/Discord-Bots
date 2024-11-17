import discord
from config import *
from pytube import Playlist

songqueue = []

intents = discord.Intents().all()
client = discord.Client(intents=intents)  

class addsong(discord.ui.Modal, title='Lied Hinzufügen'):
    
    chname = discord.ui.TextInput(
        label='Video Link / Playlist Link',
        style=discord.TextStyle.long,
        required=True,
        max_length=4000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        if not any(self.chname.value in d for d in songqueue):
            if not "playlist" in self.chname.value:
                songqueue.append(self.chname.value)
                await interaction.response.defer()
            else:
                await interaction.response.defer()
                playlist = Playlist(self.chname.value)
                await interaction.followup.send(f"ich habe {len(playlist)} Lieder in deiner Playlist gefunden!", ephemeral=True)
                for url in playlist:
                    songqueue.append(url)
        else:
            await interaction.response.send_message(f"hallo {interaction.user.name}, Das lied ist bereits in der Warteschlange!", ephemeral=True)