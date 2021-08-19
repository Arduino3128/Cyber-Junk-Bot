from discord.ext import commands,tasks
import discord
import os
import tweepy
from replit import db

consumer_key, consumer_secret=os.environ["TWITTER_CONSUMER_KEY"],os.environ["TWITTER_CONSUMER_SECRET"]
access_token, access_token_secret=os.environ["TWITTER_ACCESS_TOKEN"],os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
db["Follow"]=[]

class Twitter(commands.Cog):
	def __init__(self,bot):
		self.bot=bot

	@commands.command(name="trending", help="Get Trending Posts!")
	async def get_trending(self,ctx,trend="#cybersecurity"):
		trends_result = api.trends_place(1)
		#add to send the trending post
	
	@commands.command(name="twitter", help="Use this to delete spam messages only!")
	async def twitter_processor(self,ctx,action,who):
		if action=="follow":
			Follow=db["Follow"]
			Follow.append(who)
			db["Follow"]=Follow
			embed=discord.Embed(title="Twitter",description=f"Following {who} :sunglasses:",color=0x00FF00)

		elif action=='unfollow':
			UnFollow=db["Follow"]
			UnFollow.remove("")
			db["Follow"]=Follow
			embed=discord.Embed(title="Twitter",description=f"Unfollowed {who} :confused:",color=0x00FF00)
		ctx.send(embed=embed)

	class MyStreamListener(tweepy.StreamListener):
		def __init__(self, api):
			self.api = api
			self.me = api.me()

tweets_listener = Twitter.MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener,thread=True)
stream.filter(follow=db["Follow"], languages=["en"])




def setup(bot):
	bot.add_cog()