import discord
from discord.ext import commands

class Warning(commands.Cog):
	def __init__(self,bot):
		self.bot=bot
	
	@commands.command(name="warn", help="Only for Moderators and Admins.")
	@commands.has_permissions(kick_members=True)
	async def warn(self,ctx,who,reason=""):
		try:
			if reason!="":
				await ctx.send(content=f":warning: Warned {who}\n Reason: {reason}")
			else:
				await ctx.send(content=f":warning: Warned {who}")
		except:
			await ctx.send(content="Format: $warn <Mention_User> <Reason>")



def setup(bot):
	bot.add_cog(Warning(bot))