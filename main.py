import discord, search_that_hash,tweepy
from discord.ext import commands
import json
import os

bot = commands.Bot(command_prefix='>')

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

@bot.event
async def on_guild_join(guild):
	for channel in guild.channels:
			if str(channel)=='announcements':
				channel_id=int(channel.id)
				break
	print(channel_id)
	channel = bot.get_channel(channel_id)
	embed = discord.Embed(title="Hello! I am Cyber Junk bot :robot:",description=":wave: Get Tweet alerts from you favourite Cybersec Expert. :confetti_ball:",color=0x2E5090)
	embed.set_footer(text="I am developed by Kanad Nemade")
	await channel.send(embed=embed)

bot.run(os.environ['DISCORD_TOKEN'])