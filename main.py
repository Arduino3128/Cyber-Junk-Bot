import discord
from discord.ext import commands
import json
import os

bot = commands.Bot(command_prefix='$', intents = discord.Intents.all())

@bot.event
async def on_member_join(member):
	guild = bot.get_guild(863434765327138836)
	if (int(guild.member_count)-5) == 1000:
		channel = bot.get_channel(863434765327138843)
		await channel.send(content="""Woohoo!🎉\n🎊We have reached 1000 members on Discord!🎊\nThank You All!""",file=discord.File('./static/500.png'))

@bot.event
async def on_ready():
	with open("config/cogs.json",'r') as config:
		configs=json.load(config)
	print("⎆ Loading Cogs ⌦")
	for cog in configs["Cogs"]:
		try:
			bot.load_extension(cog)
			print(f"❖ Cog {cog} loaded successfully!")
		except Exception as error:
			print(f"⎈ Cog {cog} failed to load.")
			print(f"⎇ Debug: {error}")

	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='over the server'))

@bot.event
async def on_guild_join(guild):
	for channel in guild.channels:
			if 'announcements' in str(channel):
				channel_id=int(channel.id)
				break
	print(channel_id)
	channel = bot.get_channel(channel_id)
	embed = discord.Embed(title="Hello! I am Cyber Junk bot :robot:",description=":wave: Get Tweet alerts from you favourite Cybersec Expert. :confetti_ball:",color=0x2E5090)
	embed.set_footer(text="I am developed by Kanad Nemade")
	await channel.send(embed=embed)

#@bot.event
#async def on_command_error(ctx, error):
	#print(error)
	
bot.run(os.environ['DISCORD_TOKEN'])
