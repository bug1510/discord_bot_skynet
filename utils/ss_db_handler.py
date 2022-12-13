import sqlite3
from discord.ext import commands
from skynet_bot import ssdbpath

class DBHandler(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def create_table(self, guild_id):
        con = sqlite3.connect(f'{ssdbpath}/{guild_id}.db')
        cur = con.cursor()
        cur.execute("""Create Table IF NOT EXISTS leveling
        (dc_user_nick text, dc_user_id integer, tw_user_nick text, tw_user_id integer, level integer NOT NULL DEFAULT 1, exp integer NOT NULL DEFAULT 0)""")
        con.commit()
        con.close()

    async def create_user(self, guild_id, dc_user_id, dc_user_name):
        try:
            con = sqlite3.connect(f'{ssdbpath}/{guild_id}.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM leveling WHERE dc_user_id = $1",(dc_user_id,))
            entry = cur.fetchone()
            con.close()

            if entry:
                return
            else:
                con = sqlite3.connect(f'{ssdbpath}/{guild_id}.db')
                cur = con.cursor()
                cur.execute("INSERT INTO leveling (dc_user_nick, dc_user_id) VALUES(?, ?)",(dc_user_name, dc_user_id))
                con.commit()
                con.close()
                self.bot.logger.info(f'SingleServerDBHandlingUtils | Created New User Entry: {dc_user_name}')
        except Exception as e:
            self.bot.logger.critical(f'SingleServerDBHandlingUtils | Creating User Entry {dc_user_name} in the Database failed due to: {e}')

    async def get_user_exp_and_level(self, guild_id, dc_user_id, dc_user_name):
        await self.create_user(guild_id, dc_user_id, dc_user_name)
        try:
            con = sqlite3.connect(f'{ssdbpath}/{guild_id}.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM leveling WHERE dc_user_id = $1",(dc_user_id,))
            db_entry = cur.fetchone()
            con.close()
            return db_entry
        except Exception as e:
            self.bot.logger.warning(f'SingleServerDBHandlingUtils | failed to get User Level and Experience from User {dc_user_name} due to: {e}')
    
    async def update_user_exp(self, guild_id, dc_user_id, dc_user_name, user_lvl_exp):
        level = user_lvl_exp[0]
        exp = user_lvl_exp[1]

        try:
            con = sqlite3.connect(f'{ssdbpath}/{guild_id}.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM leveling WHERE dc_user_id = $1",(dc_user_id,))

            cur.execute("UPDATE leveling SET level = ?, exp = ? WHERE dc_user_id = ?",(level, exp, dc_user_id,))
            con.commit()
            con.close()
        except Exception as e:
            self.bot.logger.warning(f'SingleServerDBHandlingUtils | failed to update Level and Experience for User {dc_user_name} due to: {e}')

async def setup(bot):
    await bot.add_cog(DBHandler(bot))