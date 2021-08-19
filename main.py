import discord, search_that_hash,tweepy
from discord import commands
import json
import os

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
	with open("config/cogs.json",'r') as config:
		configs=json.load(config)
	print("Loading Cogs")
	for cog in configs["Cogs"]:
		try:
			bot.load_extension(cog)
			print(f"Cog {cog} loaded successfully!")
		except Exception as error:
			print(f"Cog {cog} failed to load.",str(error))
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='over the server'))

bot.run(os.environ['DISCORD_TOKEN'])