import discord
from configs import string_settings, main_Meta, user_settings, team_list

intents = discord.Intents().all()
client = discord.Client(intents=intents)  

class tiketControls(discord.ui.View):
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)
      
    @discord.ui.button(label=string_settings["clTiket"]["name"], style=string_settings["clTiket"]["color"], emoji=string_settings["clTiket"]["Emoji"], row=0)
    async def b1(self, interaction:discord.Interaction, button:discord.Button): 
        channel = interaction.channel
        user = interaction.user
        guild = client.get_guild(main_Meta["GuildID"])
        
        if user_settings["canUserCloseTiket"] == False:
            for role in team_list:
                if role in [y.id for y in user.roles]:
                    if team_list[role]["canCloseTiket"] == True:
                        member_list = [i.id for i in channel.members]

                        for memberst in member_list:
                            memberobj = guild.get_member(memberst)
                            perms = channel.overwrites_for(memberobj)
                            perms.send_messages = False
                            await channel.set_permissions(memberobj, overwrite=perms, reason="Tiket Closed")
                        
                        await channel.edit(name=f"{channel.name} closed")

                        await interaction.response.defer()
                        await channel.send(f"**This Tiket was Closed by {interaction.user.name}**")
                        return
                    
                await interaction.response.send_message("You do not have permission to Close the Tiket!", ephemeral=True)
        else:
            member_list = [i.id for i in channel.members]

            for memberst in member_list:
                memberobj = guild.get_member(memberst)
                perms = channel.overwrites_for(memberobj)
                perms.send_messages = False
                await channel.set_permissions(memberobj, overwrite=perms, reason="Tiket Closed")
                        
            await channel.edit(name=f"{channel.name} closed")
            await interaction.response.defer()
            await channel.send(f"**This Tiket was Closed by {interaction.user.name}**")


                    
            
        

    @discord.ui.button(label=string_settings["delTiket"]["name"], style=string_settings["delTiket"]["color"], emoji=string_settings["delTiket"]["Emoji"], row=0)
    async def b2(self, interaction:discord.Interaction, button:discord.Button): 
        channel = interaction.channel
        user = interaction.user
        guild = client.get_guild(main_Meta["GuildID"])
        

        for role in team_list:
            if role in [y.id for y in user.roles]:
                if team_list[role]["canDeleteTiket"] == True:
                    if "closed" in channel.name:
                        await channel.delete()
                        return
                    else:
                        await interaction.response.send_message("Pls Close the Tiket first!", ephemeral=True)
                        return
                
        await interaction.response.send_message("You do not have permission to Delete the Tiket!", ephemeral=True)

class controlsUI(discord.ui.View):
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)
      
    @discord.ui.button(label=string_settings["crTiket"]["name"], style=string_settings["crTiket"]["color"], emoji=string_settings["crTiket"]["Emoji"], row=0)
    async def b1(self, interaction:discord.Interaction, button:discord.Button):        
        user = interaction.user
        username = interaction.user.name

        guild = client.get_guild(main_Meta["GuildID"])
        channel = client.get_channel(main_Meta["channelSettings"]["tiketCategorie"])

        allTikets = discord.utils.get(channel.text_channels, name=username)
        if not allTikets:

            mainTeamRole = guild.get_role(main_Meta["mainTeamRole"])
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                user: discord.PermissionOverwrite(view_channel=True),
                mainTeamRole: discord.PermissionOverwrite(view_channel=True),
                guild.me: discord.PermissionOverwrite(view_channel=True)
            }

            tiketChannel = await guild.create_text_channel(f'{username}', category=channel, overwrites=overwrites)
            await interaction.response.send_message(f"Hello **{username}** pls descripe your problem in {tiketChannel.mention}", ephemeral=True)
            
            embed = discord.Embed(title="", color=main_Meta["controlEmbedColor"])
            embed.set_image(url=main_Meta["tiketHeadImg"])
            await tiketChannel.send(embed=embed, view=tiketControls())

            rolemention = ""
            if main_Meta["NotifyTeam"] == True:
                for roles in team_list:
                    role = guild.get_role(roles)
                    rolemention = rolemention + " " + f"{role.mention}"

                await tiketChannel.send(f"{rolemention} **Hy here is a new Tiket!**")
        else:
            await interaction.response.send_message(f"Hello **{username}** you already have a Tiket in {allTikets.mention} Pending!", ephemeral=True)
