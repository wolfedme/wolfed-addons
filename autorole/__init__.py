from .autoRole import AutoRole


def setup(bot):
	bot.add_cog(AutoNick(bot))
