import discord

from redbot.core import Config, checks, commands
from redbot.core.bot import Red
from redbot.core.commands import Context
from typing import Any

Cog: Any = getattr(commands, "Cog", object)


class LeaveMsg(Cog):
	"""
	Posts message to channel when a user leaves the Server
	"""

	def __init__(self, bot: Red):
		self.bot = bot
		self.config = Config.get_conf(self, identifier=69696969, force_registration=True)
		default_guild = {"channel": "",
		                 "channel_name": "Please set a channel with [p]leaveMsg setChannel",
		                 "message": "%s isch fort"}

		self.config.register_guild(**default_guild)

	@commands.group(aliases=["lmsg"])
	@checks.mod_or_permissions(administrator=True)
	async def leaveMsg(self, ctx: Context):
		""" Post leave messages on user leave """
		if ctx.invoked_subcommand is None:
			guild = ctx.guild
			channel = await self.config.guild(guild).channel_name()
			message = await self.config.guild(guild).message()
			await ctx.send("Posting `%s` to %s" % (message % "$username$", channel))


	@leaveMsg.command()
	async def setMessage(self, ctx: Context, msg: str):
		"""
		Sets the message the bots sends on leave
		:param ctx: Context
		:param msg: Message needs to have %s as username
		"""
		if msg != "":
			await self.config.guild(ctx.guild).message.set(msg)
			await ctx.send("Message `%s` set." % msg)
		pass

	@leaveMsg.command()
	async def setChannel(self, ctx: Context):
		"""
		Sets the channel to return the message to
		"""
		guild = ctx.guild
		await self.config.guild(guild).channel.set(ctx.channel.id)
		await self.config.guild(guild).channel_name.set(ctx.channel.name)
		await ctx.send("Posting messages to %s" % ctx.channel.name)

	@commands.Cog.listener()
	async def on_member_remove(self, member: discord.Member):
		guild = member.guild
		channel = await self.config.guild(guild).channel()

		if channel != "":
			channel = guild.get_channel(channel)
			out = await self.config.guild(guild).message()
			out = (out % member.nick)

			await channel.send(out)

		else:
			pass
