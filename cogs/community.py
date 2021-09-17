from discord.ext import commands
from discord.ext.commands.core import command
import sqlite3, json, os
from leveling.lvl import exp_gain

class ShirosSakeBar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='leveling_on')
    async def init_leveling_db(self, ctx):
        guild_id = ctx.message.author.guild.id
        con = sqlite3.connect(f'{guild_id}.db')
        cur = con.cursor()
        cur.execute("""Create Table IF NOT EXISTS leveling
        (dc_user_nick text, dc_user_id integer, tw_user_nick text, tw_user_id integer, level integer NOT NULL DEFAULT 1, exp integer NOT NULL DEFAULT 0)""")
        con.commit()
        con.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            await exp_gain(message)

def setup(bot):
    bot.add_cog(ShirosSakeBar(bot))