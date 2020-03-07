from .leaveMsg import LeaveMsg


def setup(bot):
	bot.add_cog(LeaveMsg(bot))
