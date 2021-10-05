from discord.ext import commands
import discord

class Delete(commands.Cog):
	def __init__(self,bot):
		self.bot=bot

	@commands.command(name="delete", help="Only for Moderators and Admins.")
	@commands.has_permissions(kick_members=True)
	async def deletechats(self,ctx, limit):
		async for msg in ctx.message.channel.history(limit=int(limit)+1):
			try:
				await msg.delete()
			except:
				pass
	@deletechats.error
	async def kick_error(ctx, error):
		pass
def setup(bot):
	bot.add_cog(Delete(bot))