from discord.ext import commands
import requests,re
import discord
import json

class AntiSpam(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.scammer = []
		with open("cogs/bot_files/blockwords.json") as file:
			self.phish_words=json.load(file)
		with open("cogs/bot_files/phish.db") as file:
			self.phish_db=json.load(file)
		
	@commands.Cog.listener()
	async def on_message(self, message):
		counter = 0
		url=message.content
		author = message.author
		try:
			url=re.search("(?P<url>https?://[^\s]+)", url).group("url")
			for i in self.phish_db:
				if self.phish_db[i]==url:
					counter+=4
					print(f"{url} found in Phish DB")
					break
		except:
			pass
		try:
			if counter==0 and bool(re.search("(?P<url>https?://[^\s]+)", url)):
				headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"}
				try:
					print(f"Trying direct invasion at {url}")
					text=""
					text = requests.get(url,headers=headers,allow_redirects=True).text
				except:
					phish_stat=f"https://phishstats.info:2096/api/phishing?_where=(url,like,{url})&_sort=-id"
					try:
						print(f"Trying phish stat invasion at {url}")
						phish_data=json.loads(requests.get(phish_stat,headers=headers,allow_redirects=True).text)
						score=phish_data[0]["score"]
						if score>1.5:
							counter=4
					except Exception as ERROR:
						print(ERROR)
				spams=self.phish_words['phish_words']
				msg_cont=message.content
				if "@everyone" in msg_cont:
					counter+=1
				for x in spams:
					if x in text:
						if "Nitro" in x or "Nitrо" in x:
							counter+=1
						print("Scam word detected: ", x)
						counter+=1
			if counter>3:
				print(message.author.id)
				try:
					with open('cogs/static/blacklist.txt','a') as black_list:
						black_list.write("\n\n"+str(message.content)+"------->"+str(author)+"-->"+str(message.author.id))
				except Exception as ERROR:
					print(ERROR)
				await message.delete()
				try:
					#print(f"TYPE OF DB: {type(self.phish_db)} and data is: {self.phish_db}")
					if url not in self.phish_db.values():
						print("Writing Phishing link to the DB")
						self.phish_db[str(len(self.phish_db))]=url
						with open('cogs/bot_files/phish.db','w') as file:
							json.dump(self.phish_db,file)						
				except Exception as ERROR:
					print(ERROR)
				print('Scam by', author)
				self.scammer.append(author.id)
				if self.scammer.count(author.id)>4:
					await message.channel.send(content=f':hammer: Banned {message.author.mention} \n Reason: We don\'t do that here!')
					await message.author.kick()
				elif self.scammer.count(author.id)>2:
					await message.channel.send(content=f':warning: Warned {message.author.mention} \n Reason: Spamming!')
					rolled = discord.utils.get(message.author.guild.roles,name="mute")
					await message.author.add_roles(rolled)
		except Exception as ERROR:
			print(ERROR)


def setup(bot):
	bot.add_cog(AntiSpam(bot))
