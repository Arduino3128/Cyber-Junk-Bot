from quart import Quart, render_template, redirect, request
from discord.ext import commands
import discord
import random, os
from threading import Thread

class API(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.server(bot)

	def server(self,bot):
		app = Quart(__name__, static_url_path='', static_folder='static')

		@app.route('/')
		async def home():
			return redirect("https://arduino3128.github.io/Cyber-Junk-Bot/", code=301)

		@app.errorhandler(404)
		async def page_not_found(e):
			return await render_template('404.html'), 404

		async def pick_winners(channel_id,number_to_pick,participants,message):
			channel = bot.get_channel(int(channel_id))
			for i in range(int(number_to_pick)):
				lucky_winner  = random.choice(participants)
				participants.pop(participants.index(lucky_winner))
				embed=discord.Embed(title="**Giveaway results**", description=message)
				embed.add_field(name="**The winner is**",value=f"{lucky_winner.mention}")
				embed.set_author(name="Cyber Junk", icon_url="https://arduino3128.github.io/Cyber-Junk-Bot/img/logo.png")
				await channel.send(content=f"{lucky_winner.mention}",embed=embed)

		@app.route('/api',methods=['POST','GET'])
		async def api():
			if (request.method=='POST') and (request.headers.get('User-Agent')==os.environ['USER_AGENT']):
				if (await request.form)['CORS-Key']==os.environ['CORS_KEY']:
					if (await request.form)['Type']=="SendMsg":
						message =  (await request.form)['Message']
						channel_id = (await request.form)['Channel_ID']
						channel=await bot.fetch_channel(int(channel_id))
						if channel != None:
							await channel.send(content=f"{message}")
							return "OK"
						else:
							return "ERROR"
					elif (await request.form)['Type']=="Whois":
						rep = {"<@&888418636623151114>":"Volunteer","<@&863684165567250432>":"Moderator"}
						user_id = (await request.form)['User_ID']
						guild = bot.get_guild(863434765327138836)
						user = await guild.fetch_member(int(user_id))
						try:
							mention = [role.mention for role in user.roles if str(role.mention) == "<@&863684165567250432>" or str(role.mention) == "<@&888418636623151114>"]
							if mention!=[]:
								if "<@&863684165567250432>" in mention:
									return rep["<@&863684165567250432>"]
								elif "<@&888418636623151114>" in mention:
									return rep["<@&888418636623151114>"]
							return "None"
						except:
							return "None"

					elif (await request.form)['Type']=="Pick_Giveaway":
						message_id =  (await request.form)['Message_ID']
						number =  (await request.form)['Number']
						channel_id = (await request.form)['Channel_ID']
						channel=bot.get_channel(int(channel_id))
						if channel != None:
							message = await channel.fetch_message(message_id)
							for i in message.embeds:
								message_body = i.description
							users = await message.reactions[0].users().flatten()
							users.pop(users.index(bot.user))
							await pick_winners(channel_id,number,users,message_body)
							return "OK"
						else:
							return "ERROR"
					elif (await request.form)['Type']=="Create_Poll":
						emojis=["🇦","🇧","🇨","🇩","🇪","🇫","🇬","🇭","🇮","🇯","🇰","🇱","🇲","🇳","🇴","🇵","🇶","🇷","🇸","🇹","🇺","🇻","🇼","🇽","🇾","🇿"]
						content =  (await request.form)['Content']
						channel_id = (await request.form)['Channel_ID']
						options = (await request.form)['Options']
						options = options.split("|")
						channel=bot.get_channel(int(channel_id))
						if channel != None:
							embed = discord.Embed(title="**Poll**", description=content)
							for i in range(len(options)):
								embed.add_field(name=f":regional_indicator_{chr(97+i)}:",value=options[i])
							message = await channel.send(embed=embed)
							for i in range(len(options)):
								await message.add_reaction(emojis[i])
							return "OK"
						else:
							return "ERROR"

					elif (await request.form)['Type']=="Create_Giveaway":
						content =  (await request.form)['Content']
						channel_id = (await request.form)['Channel_ID']
						channel=bot.get_channel(int(channel_id))
						if channel != None:
							embed=discord.Embed(title="**Giveaway**", description=content)
							embed.set_author(name="Cyber Junk", icon_url="https://arduino3128.github.io/Cyber-Junk-Bot/img/logo.png")
							message = await channel.send(embed=embed)
							await message.add_reaction("🎉")
							return "OK"
						else:
							return "ERROR"
				else:
					return await render_template('404.html'), 404
			else:
				return await render_template('404.html'), 404
		def run():
			try:
				print("⎆ Web Server started.")
				bot.loop.create_task(app.run_task(host="0.0.0.0", port=8080))
			except Exception as error:
				print("⎈ Failed to start Web Server.")
				print(f"⎇ Debug: {error}")

		def keep_alive():
			print("⎆ Starting Web Server.....")
			t=Thread(target=run)
			t.start()
		keep_alive()

def setup(bot):
	bot.add_cog(API(bot))