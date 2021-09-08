import discord
from discord.ext import commands

class Rules(commands.Cog):
	def __init__(self,bot):
		self.bot=bot
	
	@commands.command(name="rule",help="Display Server rules")
	async def rule(self,ctx,number="-1"):
		with open("config/rules.txt",'r') as rules:
			rules=rules.read()
		rules=rules.split("\n")
		try:
			if int(number)<=0:
				rules=[f"{i+1}. {rules[i]}" for i in range(len(rules)) ]
				rules="\n".join(rules)
				await ctx.send(content=f"__**Rules:**__\n{rules}")
			else:
				try:
					number=abs(int(number))
					await ctx.send(content=f"__**Rule {number}**__: {rules[number-1]}")
				except:
					await ctx.send(content="Format: $rule <RULE_NUMBER>")
		except:
				await ctx.send(content="Format: $rule <RULE_NUMBER>")


def setup(bot):
	bot.add_cog(Rules(bot))