import discord
from discord.colour import Color
main_Meta = {
    "BotToken": "TOKEN",
    "BotName": "TiketBot",
    "BotActivity": "Managing Tikets",
    "GuildID": 12345, #Guild ID
    "mainTeamRole": 12345, #Role that every Teamember has
    "channelSettings": {
        "tiketCategorie": 12345, #Category unter what the tikets gets created
        "tiketControlChannel": 12345 #Control channel for the system
    },
    "NotifyTeam": True, #Notify teammembers of new tikets listet under team_list
    "controlHeadImg": "https://cdn.pixabay.com/photo/2015/08/23/09/22/banner-902589_640.jpg",
    "tiketHeadImg": "https://cdn.pixabay.com/photo/2015/08/23/09/22/banner-902589_640.jpg",

    # Color Stuff
    "controlEmbedColor": discord.Color.blurple()
}

team_list = {
    12345: { #Add your Team Roles you want to add Perms for
        "canCloseTiket": True,
        "canDeleteTiket": True
    }
}

user_settings = { #If True, All Permissions above are Ignored!
    "canUserCloseTiket": False
}

string_settings = {
    "crTiket": {
        "name": "Create Tiket",
        "Emoji": "✅",
        "color": discord.ButtonStyle.green
    },
    "clTiket": {
        "name": "Close Tiket",
        "Emoji": "✖️",
        "color": discord.ButtonStyle.red
    },
    "delTiket": {
        "name": "Delete Tiket",
        "Emoji": "📋",
        "color": discord.ButtonStyle.blurple
    }
}