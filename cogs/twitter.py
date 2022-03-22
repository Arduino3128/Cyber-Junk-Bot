from discord.ext import commands,tasks
import discord
import os
import tweepy
from pymongo import MongoClient
from datetime import date

Cluster = MongoClient(os.environ['MONGO_DB'])
Database=Cluster["cyber_junk_bot"]
Collection=Database["twitter"]
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
		try:
			tweets = tweepy.Cursor(api.search,
        	      q=trend,
        	      lang="en",
        	      since=str(date.today())).items(1)
			for tweet in tweets:
				tweet=tweet
			tweet=tweet.__dict__['_json']
			await ctx.send(content=f"https://twitter.com/{str(tweet['user']['screen_name'])}/status/{str(tweet['id'])}")
		except:
			pass

	@commands.command(name="twitter", help="Format:- $twitter follow/unfollow <Username>")
	async def twitter_processor(self,ctx,action,who):
		try:
			Followed=Collection.find()
			Followed=[x for x  in Followed]
			if "@" in who:
				who=who.replace("@","")
			if action=="follow":
				try:
					api.lookup_users(screen_name=who)
					Username=Collection.find_one({"Username":who})
					if Username==[] or Username==None:
						Collection.insert_one({"Username":who,"ID":""})
						embed=discord.Embed(title="Twitter",description=f"Following {who} :sunglasses:",color=0x00FF00)
					else:
						embed=discord.Embed(title="Twitter",description=f"Already Following {who} :sunglasses:",color=0x00FF00)
				except:
					embed=discord.Embed(title="Twitter",description=f"Could not find {who} :confused:",color=0xFF0000)
			elif action=='unfollow':
				Collection.delete_one({"Username":who})
				embed=discord.Embed(title="Twitter",description=f"Unfollowed {who} :confused:",color=0x00FF00)
			await ctx.send(embed=embed)
		except:
			pass

	@tasks.loop(seconds=15)
	async def fetch_from_followers(self):
		try:
			users=Collection.find()
			for user in users:
				tweets=tweepy.Cursor(api.user_timeline,
				screen_name=user['Username'],
				exclude_replies=True,
				lang="en",
				since=str(date.today())).items(1)
				for tweet in tweets:
					tweet=tweet
					temp=tweet.__dict__
				if (str(tweet.id)==str(user["ID"]) or temp['_json']['text'][0:4]=="RT @"):
					pass
				else:
					channel=self.bot.get_channel(863442157343342658)
					await channel.send(content=f'@{temp["user"].__dict__["_json"]["name"]} Tweeted:\nhttps://twitter.com/{str(temp["user"].__dict__["_json"]["screen_name"])}/status/{str(tweet.id)}')
					Collection.update_one({"Username":user['Username']},{"$set":{"ID":str(tweet.id)}})
		except:
			pass

def setup(bot):
	bot.add_cog(Twitter(bot))