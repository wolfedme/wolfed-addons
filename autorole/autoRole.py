from typing import Any
import discord

from redbot.core import commands, Config

Cog: Any = getattr(commands, "Cog", object)


class AutoRole(Cog):
	"""Auto role assign and auto renaming based on role. Currently only on joining"""

	def __init__(self, bot):
		self.bot = bot
		self.config = Config.get_conf(self, identifier=69696969)
		default_guild = {"joinChar": "🥨",
		                 "joinRole": "",
						 "logChannel": "",
						 }

		self.config.register_guild(**default_guild)

	@commands.guild_only()
	@commands.mod_or_permissions(administrator=True)
	@commands.group()
	@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
	async def autoRole(self, ctx):
		pass

	@autonick.command()
	async def onJoin(self, ctx, char, role: discord.Role):
		"""Define the emoji which gets added in front of a new users nickname. Syntax: `[p]autoRole onJoin [nicknamePrefix] [role]`"""
		if char == "":
			await ctx.send("Empty prefix")
			pass
		if role == "":
			await ctx.send("Empty role")
			pass
		if role != discord.Role:
			await ctx.send("Role is not a discord.Role!")
			pass

		await self.config.guild(guild).joinRole.set(role)
		await ctx.send("Added prefix %s for role %s on _join_" % (char, role.name))

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
		prefix = await self.config.guild(guild).joinChar()
		nickname = "%s %s" % (prefix, nickname)
		loggingChannel = await self.config.guild(guild).logChannel()
		loggingChannel = guild.get_channel(loggingChannel)
		joinRole = await self.config.guild(guild).joinRole()
		joinRoleName = await self.config.guild(guild).joinRoleName()

		await member.edit(nick=nickname, role=joinRole)
		await loggingChannel.send("Changed nickname of %s with prefix %s and assigned role %s" % (member.name, prefix, joinRole.name))
