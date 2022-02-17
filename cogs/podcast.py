import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
from discord.ext import commands
import discord
from discord import FFmpegPCMAudio
import json


class Podcast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.volume = 100

    @commands.command(
        name="join", help="Ask Cyber Junk bot to join current voice channel"
    )
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(
        name="leave", help="Ask Cyber Junk bot to leave current voice channel"
    )
    async def leave(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()

    @commands.command(name="pause", help="Ask Cyber Junk bot to pause current podcast")
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()

    @commands.command(name="resume", help="Ask Cyber Junk bot to resume podcast")
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()

    @commands.command(
        name="stop", help="Ask Cyber Junk bot to stop playing current podcast"
    )
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()

    @commands.command(name="volume", help="Set volume of the podcast")
    async def volume(self, ctx, volume):
        print(self.volume)
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = int(voice.source.volume)+int(volume) / 100
        print("Current Volume: ", voice.source.volume)
        self.volume = int(volume)

    @commands.command(
        name="podcast",
        help="Listen to podcasts from H3unt3d Hacker and Darknet Diaries",
    )
    async def listen(self, ctx, whom, search_terms):
        embed = discord.Embed(
            title="Podcast",
            description=f"Searching for {search_terms} podcast :mag: ",
            color=0x00FFFF,
        )
        message = await ctx.send(embed=embed)
        FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 ",
            "options": "-vn",
        }
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if whom == "haunted":
            URL = "https://podcastaddict.com/podcast/3359596"
            response = requests.get(
                URL,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"
                },
            )
            soup3 = BeautifulSoup(response.text, "html.parser")
            spans = soup3.findAll("h5")
            show = (
                str(spans[int(search_terms) - 1])
                .replace("<h5>", "")
                .replace("</h5>", "")
            )
            urls = soup3.findAll(class_="clickeableItem")
            x = (
                re.findall(r'"https:.*"', str(urls[int(search_terms) - 1]))[0]
                .replace('"https://podcastaddict.com/episode/', "")
                .replace('&amp;podcastId=3359596"', "")
            )
            urls = unquote(x)
            if urls != "":
                if not voice.is_playing():
                    embed = discord.Embed(
                        title="Podcast",
                        description=f"Now Streaming {show}",
                        color=0x00FF00,
                    )
                    embed.set_footer(
                        text="The podcast belongs to H3unt3d Hacker. Support H3unt3d Hacker at https://thehauntedhacker.com/ "
                    )
                    voice.play(FFmpegPCMAudio(urls, **FFMPEG_OPTIONS))
                    voice.source = discord.PCMVolumeTransformer(
                        voice.source, volume=1.0
                    )
                else:
                    embed = discord.Embed(
                        title="Podcast",
                        description=f"Already Streaming a Podcast. Use `$stop` to stop the podcast",
                        color=0x0000FF,
                    )
                await message.edit(embed=embed)
            else:
                embed = discord.Embed(
                    title="Podcast",
                    description=f"Could not find podcast containing {search_terms}",
                    color=0xFF0000,
                )
                await message.edit(embed=embed)

        elif whom == "darknet":
            URL = "https://f7ze6bz21v-1.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia for vanilla JavaScript (lite) 3.24.9;instantsearch.js 2.6.0;JS Helper 2.24.0&x-algolia-application-id=F7ZE6BZ21V&x-algolia-api-key=9e3eb8ec69f6c9eda40fc76d316d88f2"
            header = {
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
            }
            data = {
                "requests": [
                    {
                        "indexName": "DarknetDiaries",
                        "params": f"query={search_terms}&page=0&facets=[]&tagFilters=",
                    }
                ]
            }
            output = requests.post(URL, json=data, headers=header)
            output = json.loads(output.text)
            if output["results"][0]["hits"] != []:
                mp3_link = output["results"][0]["hits"][0]["mp3_url"]
                page_url = output["results"][0]["hits"][0]["url"]
                podcast_title = output["results"][0]["hits"][0]["title"]
                await message.edit(content=f"https://darknetdiaries.com{page_url}")
                if not voice.is_playing():
                    embed = discord.Embed(
                        title="Podcast",
                        description=f"Now Streaming {podcast_title}",
                        color=0x00FF00,
                    )
                    embed.set_footer(
                        text="The podcast belongs to Darknet Diaries. Support Darknet Diaries at https://darknetdiaries.com/ "
                    )
                    voice.play(FFmpegPCMAudio(mp3_link, **FFMPEG_OPTIONS))
                    voice.source = discord.PCMVolumeTransformer(
                        voice.source, volume=1.0
                    )
                else:
                    embed = discord.Embed(
                        title="Podcast",
                        description=f"Already Streaming a Podcast. Use `$stop` to stop the podcast",
                        color=0x0000FF,
                    )
                await message.edit(embed=embed)
            else:
                embed = discord.Embed(
                    title="Podcast",
                    description=f"Could not find podcast containing {search_terms}",
                    color=0xFF0000,
                )
                await message.edit(embed=embed)
        else:
            embed = discord.Embed(
                title="Podcast",
                description=f'Format: $podcast haunted|darknet "Podcast Number" :mag: ',
                color=0x00FFFF,
            )
            await message.edit(embed=embed)

    @commands.command(
        name="haunted",
        help="List Podcasts from H3unt3d Hacker",
    )
    async def haunted(self, ctx, page=1):

        embed = discord.Embed(
            title="Podcast List | H3unt3d Hacker",
            description="Fetching Podcast List..",
            color=0x00FFFF,
        )
        embed.set_footer(
            text="The podcast belongs to H3unt3d Hacker. Support H3unt3d Hacker at https://thehauntedhacker.com/ "
        )
        message = await ctx.send(embed=embed)
        try:
            Haunted_URL = "https://podcastaddict.com/podcast/3359596"
            response = requests.get(
                Haunted_URL,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"
                },
            )
            soup3 = BeautifulSoup(response.text, "html.parser")
            spans = soup3.findAll("h5")
            podcast_list = []
            for i in range((int(page) * 5) - 5, int(page) * 5):
                show = str(spans[i]).replace("<h5>", "")
                show = show.replace("</h5>", "")
                show = str(i + 1) + " ---> " + show
                podcast_list.append(show)
            podcast_list = "\n".join(podcast_list)
            embed = discord.Embed(
                title="Podcast List | H3unt3d Hacker",
                description=f"Page {page}\n" + podcast_list,
                color=0x00FF00,
            )
            embed.set_footer(
                text="The podcast belongs to H3unt3d Hacker. Support H3unt3d Hacker at https://thehauntedhacker.com/ "
            )

        except Exception as ERROR:
            print(ERROR)
            embed = discord.Embed(
                title="Podcast List | H3unt3d Hacker",
                description="Could not fetch Podcast List",
                color=0xFF0000,
            )
            embed.set_footer(
                text="The podcast belongs to H3unt3d Hacker. Support H3unt3d Hacker at https://thehauntedhacker.com/ "
            )
        await message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Podcast(bot))
