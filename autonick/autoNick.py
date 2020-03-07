from typing import Any
import discord

from redbot.core import commands, Config

Cog: Any = getattr(commands, "Cog", object)


class AutoNick(Cog):
	"""Auto renaming based on role. Currently only on joining"""

	def __init__(self, bot):
		self.bot = bot
		self.config = Config.get_conf(self, identifier=69696969)
		default_guild = {"onJoinChar": "🥨",
		                 "logChannel": ""}

		self.config.register_guild(**default_guild)

	@commands.guild_only()
	@commands.mod_or_permissions(administrator=True)
	@commands.group()
	async def autonick(self, ctx):
		pass

	@autonick.command()
	async def joinEmoji(self, ctx, msg):
		"""Define the emoji which gets added in front of a new users nickname"""
		await ctx.send("Doing nothing")

	@autonick.command()
	async def add(self, ctx):
		""" Add role to auto rename """
		await ctx.send("Still doing nothing.")

	@autonick.command()
	async def remove(self, ctx):
		""" Remove role to auto rename """
		await ctx.send("Still doing nothing.")

	@autonick.command()
	async def list(self, ctx):
		""" List all active roles for auto renaming """
		await ctx.send("Still doing nothing.")

	@autonick.command()
	async def setLog(self, ctx):
		""" Set the channel to send logs to """
		guild = ctx.guild
		await self.config.guild(guild).logChannel.set(ctx.channel.id)
		await ctx.send("Logging to %s" % ctx.channel.name)

	@commands.Cog.listener()
	async def on_member_join(self, member: discord.Member):
		guild = member.guild
		nickname = member.display_name
		prefix = await self.config.guild(guild).onJoinChar()
		nickname = "%s %s" % (prefix, nickname)
		loggingChannel = await self.config.guild(guild).logChannel()
		loggingChannel = guild.get_channel(loggingChannel)

		await member.edit(nick=nickname)
		await loggingChannel.send("Changed nickname of %s with prefix %s" % (member.display_name, prefix))
