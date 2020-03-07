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
		                 "message": "%s isch fort"}

		self.config.register_guild(**default_guild)

	@commands.group(aliases=["lmsg"])
	@checks.mod_or_permissions(administrator=True)
	async def leaveMsg(self, ctx: Context):
		""" Mother? """
		# TODO: return current settings
		if ctx.invoked_subcommand is None:
			guild = ctx.guild
			channel = await self.config.guild(guild).channel()
			message = await self.config.guild(guild).message()
			await ctx.send("Posting %s to %s" % (message % "$username$", channel))


	@leaveMsg.command()
	async def setMessage(self, ctx: Context):

		pass

	@leaveMsg.command()
	async def setChannel(self, ctx: Context):
		"""
		Sets the channel to return the message to
		"""
		guild = ctx.guild
		await self.config.guild(guild).channel.set(ctx.channel.id)
		await ctx.send("Posting messages to %s" % ctx.channel.name)

	@commands.Cog.listener()
	async def onLeave(self, member: discord.Member):
		guild = member.guild
		channel = await self.config.guild(guild).channel()

		if channel != "":
			channel = guild.get_channel(channel)
			out = await self.config.guild(guild).message()
			out = (out % member.nick)

			if await self.bot.embed_requested(channel, member):
				await channel.send(embed=discord.Embed(description=out, color=self.bot.color))
			else:
				await channel.send(out)

		else:
			pass
