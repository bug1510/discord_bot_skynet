from discord.ext import commands
from discord.ext.commands.core import command
import sqlite3, json, os
from leveling.lvl import exp_gain

class CommunityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            await exp_gain(message)

def setup(bot):
    bot.add_cog(CommunityCommands(bot))