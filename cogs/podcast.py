from discord.ext import commands
import discord
from discord import FFmpegPCMAudio
import requests
import json

class Podcast(commands.Cog):
	def __init__(self,bot):
		self.bot=bot
	@commands.command(name="join",help="Ask Cyber Junk bot to join current voice channel")
	async def join(self,ctx):
		channel=ctx.message.author.voice.channel
		await channel.connect()

	@commands.command(name="leave",help="Ask Cyber Junk bot to leave current voice channel")
	async def leave(self,ctx):
		voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
		if voice.is_connected():
			await voice.disconnect()

	@commands.command(name="pause",help="Ask Cyber Junk bot to pause current podcast")
	async def pause(self,ctx):
		voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
		if voice.is_playing():
			voice.pause()

	@commands.command(name="resume",help="Ask Cyber Junk bot to resume podcast")
	async def resume(self,ctx):
		voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
		if voice.is_paused():
			voice.resume()

	@commands.command(name="stop",help="Ask Cyber Junk bot to stop playing current podcast")
	async def stop(self,ctx):
		voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
		voice.stop()

	@commands.command(name="volume",help="Set volume of the podcast")
	async def volume(self,ctx,volume):
		voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
		voice.source = discord.PCMVolumeTransformer(voice.source)
		voice.source.volume=int(volume)/100

	@commands.command(name="podcast",help="Listen to podcasts from Darknet Diaries")
	async def listen(self,ctx,search_terms):
		embed=discord.Embed(title="Podcast",description=f"Searching for {search_terms} podcast :mag: ",color=0x00FFFF)
		message=await ctx.send(embed=embed)
		URL = "https://f7ze6bz21v-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia for vanilla JavaScript (lite) 3.24.9;instantsearch.js 2.6.0;JS Helper 2.24.0&x-algolia-application-id=F7ZE6BZ21V&x-algolia-api-key=9e3eb8ec69f6c9eda40fc76d316d88f2"
		header = {
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site"
}
		data = {
    "requests": [
        {
            "indexName": "DarknetDiaries",
            "params": f"query={search_terms}&page=0&facets=[]&tagFilters="
        }
    ]
}
		output=requests.post(URL,json=data,headers=header)
		output=json.loads(output.text)
		if output["results"][0]["hits"]!=[]:
			mp3_link=output["results"][0]["hits"][0]['mp3_url']
			page_url=output["results"][0]["hits"][0]['url']
			podcast_title=output["results"][0]["hits"][0]['title']
			await message.edit(content=f"https://darknetdiaries.com{page_url}")
			FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 ', 'options': '-vn'}
			voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
			if not voice.is_playing():
				embed=discord.Embed(title="Podcast",description=f"Now Streaming {podcast_title}",color=0x00FF00)
				embed.set_footer(text='The podcast belongs to Darknet Diaries. Support Darknet Diaries at https://darknetdiaries.com/ ')
				await message.edit(embed=embed)
				voice.play(FFmpegPCMAudio(mp3_link, **FFMPEG_OPTIONS))
				voice.is_playing()
			else:
				embed=discord.Embed(title="Podcast",description=f"Already Streaming a Podcast. Use `$stop` to stop the podcast",color=0x0000FF)
				await message.edit(embed=embed)
				return
		else:
			embed=discord.Embed(title="Podcast",description=f"Could not find podcast containing {search_terms}",color=0xFF0000)
			await message.edit(embed=embed)


def setup(bot):
	bot.add_cog(Podcast(bot))
