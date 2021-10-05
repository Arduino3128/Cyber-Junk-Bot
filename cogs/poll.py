from discord.ext import commands
from quickchart import QuickChart

class Poll(commands.Cog):
	def __init__(self,bot):
		self.bot=bot
	
	@commands.command(name="poll", help="Get result of a poll. Format: $poll MESSAGE_ID")
	async def info(self,ctx,message_id):
		channel = ctx.channel
		message = await channel.fetch_message(message_id)
		data=[]
		for i in range(len(message.reactions)):
			data.append(len(await message.reactions[i].users().flatten()))
		print(data)
		qc = QuickChart()
		qc.width = 500
		qc.height = 300
		qc.device_pixel_ratio = 1.0
		qc.config = {
		    "type": "horizontalBar",
		    "data": {
		        "labels": [chr(65+x) for x in range(len(data))],
		        "datasets": [{
		            "label": "Poll Result",
		            "data": data
		        }]
		    }
		}

		await ctx.send(content=qc.get_url())
def setup(bot):
	bot.add_cog(Poll(bot))