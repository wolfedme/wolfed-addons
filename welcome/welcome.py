import discord

from redbot.core import Config, checks, commands
from redbot.core.bot import Red
from redbot.core.commands import Context
from typing import Any

Cog: Any = getattr(commands, "Cog", object)


# TODO: Refactor functions for more intuitive use

class Welcome(Cog):
	"""
	Posts message to channel when a user leaves the Server
	"""

	def __init__(self, bot: Red):
		self.bot = bot
		self.config = Config.get_conf(self, identifier=69696969, force_registration=True)
		default_guild = {"channel":      "",
		                 "channel_name": "Please set a channel with [p]welcome setChannel",
						 "joinMessage": "%s hat Freibier dabei",
		                 "leaveMessage": "%s isch fort"}

		self.config.register_guild(**default_guild)

	@commands.group()
	@checks.mod_or_permissions(administrator=True)
	async def welcome(self, ctx: Context):
		""" Post leave messages on user leave """
		if ctx.invoked_subcommand is None:
			guild = ctx.guild
			channel = await self.config.guild(guild).channel_name()
			joinMessage = await self.config.guild(guild).joinMessage()
			leaveMessage = await self.config.guild(guild).leaveMessage()
			await ctx.send("Posting `%s` and `%s` to %s" % (leaveMessage % "$username$", welcomeMessage % "$username$", channel))

	@welcome.command()
	async def setJoinMessage(self, ctx: Context, msg: str):
		"""
		Sets the message the bots sends on leave. Syntax is [p]welcome setMessage "%s has left"
		:param ctx: Context
		:param msg: Message needs to have %s as username
		"""
		if msg != "":
			await self.config.guild(ctx.guild).joinMessage.set(msg)
			await ctx.send("Leave message `%s` set." % msg)
		pass
	
	@welcome.command()
	async def setLeaveMessage(self, ctx: Context, msg: str):
		"""
		Sets the message the bots sends on leave. Syntax is [p]welcome setMessage "%s has left"
		:param ctx: Context
		:param msg: Message needs to have %s as username
		"""
		if msg != "":
			await self.config.guild(ctx.guild).leaveMessage.set(msg)
			await ctx.send("Leave message `%s` set." % msg)
		pass

	@welcome.command()
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
			out = await self.config.guild(guild).leaveMessage()
			out = (out % member.nick)

			await channel.send(out)

		else:
			pass

	@commands.Cog.listener()
	async def on_member_join(self, member: discord.Member):
		guild = member.guild
		channel = await self.config.guild(guild).channel()

		if channel != "":
			channel = guild.get_channel(channel)
			out = await self.config.guild(guild).joinMessage()
			out = (out % member.nick)

			await channel.send(out)

		else:
			pass
