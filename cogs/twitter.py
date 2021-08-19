from discord.ext import commands,tasks
import discord
import os
import tweepy
from replit import db 
from datetime import date

consumer_key, consumer_secret=os.environ["TWITTER_CONSUMER_KEY"],os.environ["TWITTER_CONSUMER_SECRET"]
access_token, access_token_secret=os.environ["TWITTER_ACCESS_TOKEN"],os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
class Twitter(commands.Cog):
	def __init__(self,bot):
		self.bot=bot
		self.fetch_from_followers.start()

	@commands.command(name="latest", help="Get Latest Tweets!")
	async def get_trending(self,ctx,trend="#cybersec"):
		tweets = tweepy.Cursor(api.search,
              q=trend,
              lang="en",
              since=str(date.today())).items(1)
		for tweet in tweets:
			tweet=tweet
		await ctx.send(content="https://twitter.com/i/web/status/"+str(tweet.id))
	
	@commands.command(name="twitter", help="Format:- >twitter follow/unfollow <Username>")
	async def twitter_processor(self,ctx,action,who):
		if action=="follow":
			try:
				api.lookup_users(screen_name=who)
				db[who]=""
				embed=discord.Embed(title="Twitter",description=f"Following {who} :sunglasses:",color=0x00FF00)
			except:
				embed=discord.Embed(title="Twitter",description=f"Could not find {who} :confused:",color=0xFF0000)
		elif action=='unfollow':
			del db[who]
			embed=discord.Embed(title="Twitter",description=f"Unfollowed {who} :confused:",color=0x00FF00)
		await ctx.send(embed=embed)

	@tasks.loop(seconds=15)
	async def fetch_from_followers(self):
		users=[x for x in db.keys()]
		for user in users:
			tweets=tweepy.Cursor(api.user_timeline,
			screen_name=user,
			lang="en",
			since=str(date.today())).items(1)
			for tweet in tweets:
				tweet=tweet
				temp=tweet.__dict__
			if str(tweet.id)==str(db[user]):
				pass
			else:
				channel=self.bot.get_channel(859479104860717097)
				await channel.send(content=f'@{temp["user"].__dict__["_json"]["name"]} Tweeted:\nhttps://twitter.com/i/web/status/{str(tweet.id)}')
				db[user]=str(tweet.id)


def setup(bot):
	bot.add_cog(Twitter(bot))