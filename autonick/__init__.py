from .autoNick import AutoNick


def setup(bot):
	bot.add_cog(AutoNick(bot))
