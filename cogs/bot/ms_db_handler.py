import logging
from discord.ext import commands
from config_handler import ConfigHandlingUtils as cohu
from pymongo import MongoClient
import urllib.parse as up

class MultiServerDatabaseHandler(commands.Cog):
    def __init__(self) -> None:
        self.logger = logging.getLogger('SkyNet-Core.DBHandler')
        self.config = cohu().json_handler(filename=str('config.json'))
        self.dbusername = up.quote_plus(str(self.config['DBUsername']))
        self.dbpassword = up.quote_plus(str(self.config['DBPassword']))
        self.dbhost = str(self.config['DBHost'])
        self.dbport = str(self.config['DBPort'])
        self.dbclient = MongoClient("mongodb://%s:%s@%s:%s" % (self.username, self.password, self.host, self.port))

    async def create_user(self, guild_id, dc_user_id, dec_user_name):
        pass

    async def get_user_exp_and_level(self, guild_id, dc_user_id, dc_user_name):
        pass

    async def update_user_exp_and_level(self, guild_id, dc_user_id, dc_user_name, user_lvl_exp):
        pass

async def setup(bot):
    await bot.add_cog(MultiServerDatabaseHandler(bot))