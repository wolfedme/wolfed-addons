from redbot.core import commands


class AutoNick(commands.cog):
	"""Auto renaming based on role"""

	@commands.command()
	async def mycom(self, ctx):
		"""Does nothing"""
		await ctx.send("Doing nothing")
