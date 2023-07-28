import discord

intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.presences = False
intents.message_content = True