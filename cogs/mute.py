import discord
from discord.ext import commands


class Mute(commands.Cog):
	def __init__(self,bot):
		self.bot=bot
	
	@commands.command(name="mute",help="Only for Mods and Admins!")
	@commands.has_permissions(kick_members=True)
	async def mute(self,ctx,who: discord.Member,reason=''):
		rolled = discord.utils.get(ctx.guild.roles,name="mute")
		await who.add_roles(rolled)
		if reason=="":
			await ctx.send(f"🔇 Muted {who.mention}")
		else:
			await ctx.send(f"🔇 Muted {who.mention}\nReason: {reason}")
	
	@commands.command(name="unmute",help="Only for Mods and Admins!")
	@commands.has_permissions(kick_members=True)
	async def unmute(self,ctx,who: discord.Member):
		rolled = discord.utils.get(ctx.guild.roles,name="mute")
		await who.remove_roles(rolled)
		await ctx.send(f"🔈 Unmuted {who.mention}")

def setup(bot):
	bot.add_cog(Mute(bot))