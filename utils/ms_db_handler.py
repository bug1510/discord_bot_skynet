import urllib.parse as up
from discord.ext import commands
from pymongo import MongoClient

class DBHandler(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def init_db_client(self):
        self.config = cohu().json_handler(filename=str('config.json'))
        self.dbusername = up.quote_plus(str(self.config['DBUsername']))
        self.dbpassword = up.quote_plus(str(self.config['DBPassword']))
        self.dbhost = str(self.config['DBHost'])
        self.dbport = str(self.config['DBPort'])
        self.dbclient = MongoClient("mongodb://%s:%s@%s:%s" % (self.username, self.password, self.host, self.port))

        guild_id = ctx.message.author.guild.id
        
        try:
            mydb = self.dbclient[str(guild_id)]
            mycol = mydb["serverconfig"]
            mycol.insert_one(self.config)

            for y in mycol.find():
                print(y) 

            embed.add_field(
                name= '!Success creating Leveling Database!',
                value= 'Die Level Datenbank wurde angelegt.',
                inline= False
            )
            embed.add_field(
                name= '!Failure creating Leveling Database',
                value= f'Die Level Datenbank konnte nicht angelegt werden. \n{e}',
                inline= False
            )
        except Exception as e:
            self.bot.logger.critical(f'MultiServerDatabaseHandler | Initiating the Database Client failed due to: {e}')
    
    async def create_table(self, guild_id):
        pass

    async def create_user(self, guild_id, dc_user_id, dec_user_name):
        pass

    async def get_user_exp_and_level(self, guild_id, dc_user_id, dc_user_name):
        pass

    async def update_user_exp_and_level(self, guild_id, dc_user_id, dc_user_name, user_lvl_exp):
        pass

async def setup(bot):
    await bot.add_cog(DBHandler(bot))