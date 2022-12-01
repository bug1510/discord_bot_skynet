import sqlite3, os, logging
from utils.bot.config_handler import ConfigHandlingUtils as cohu

class SingleServerLevelHandlingUtils():
    def __init__(self) -> None:
        self.logger = logging.getLogger('SkyNet-Core.Leveling_Utils')
        self.source = os.path.dirname(os.path.abspath(__file__))
        self.config = cohu().json_handler(filename=str('config.json'))

    async def create_user(self, message):
        guild_id = message.author.guild.id
        dc_user_id = message.author.id
        dc_user_nick = message.author

        con = sqlite3.connect(f'{self.source}/../../data/{guild_id}.db')
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM leveling WHERE dc_user_id = $1",
            (dc_user_id,))
        entry = cur.fetchone()
        con.close()

        if entry:
            return
        else:
            con = sqlite3.connect(f'{self.source}/../../data/{guild_id}.db')
            cur = con.cursor()
            cur.execute(
                "INSERT INTO leveling (dc_user_nick, dc_user_id) VALUES(?, ?)",
                (str(dc_user_nick), dc_user_id))
            con.commit()
            con.close()

    async def exp_gain(self, message, rate):
        guild_id = message.author.guild.id
        dc_user_id = message.author.id

        if os.path.exists(f'{self.source}/../../data/{str(guild_id)}.db'):
            await self.create_user(message = message)

            con = sqlite3.connect(f'{self.source}/../../data/{guild_id}.db')
            cur = con.cursor()

            cur.execute(
                "SELECT * FROM leveling WHERE dc_user_id = $1",
                (dc_user_id,))
            entry = cur.fetchone()

            exp = entry[5]
            level = entry[4]

            if level == self.config['maxLevel']:
                return
            elif level < 2:
                new_level = int((exp + rate) / (100 * 2 ** (level - 1)))
            else:
                new_level = int((exp + rate) / (100 * 2 ** (level - 2)))
            
            if new_level > level:
                new_level = new_level
                exp = 0
            else:
                new_level = level

            cur.execute(
                "UPDATE leveling SET level = ?, exp = ? WHERE dc_user_id = ?",
                (new_level, exp + rate, dc_user_id,))
            con.commit()
            con.close()
        else:
            return

    async def get_rank(self, ctx):
        guild_id = ctx.message.author.guild.id
        dc_user_id = ctx.message.author.id

        con = sqlite3.connect(f'{self.source}/../../data/{guild_id}.db')
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM leveling WHERE dc_user_id = $1",
            (dc_user_id,))
        entry = cur.fetchone()
        con.close()

        return entry