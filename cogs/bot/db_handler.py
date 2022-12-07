import logging
from config_handler import ConfigHandlingUtils as cohu
from pymongo import MongoClient
import urllib.parse as up

class DBHandler():
    def __init__(self) -> None:
        self.logger = logging.getLogger('SkyNet-Core.DBHandler')
        self.config = cohu().json_handler(filename=str('config.json'))
        self.username = up.quote_plus(str(self.config['DBUsername']))
        self.password = up.quote_plus(str(self.config['DBPassword']))
        self.host = str(self.config['DBHost'])
        self.port = str(self.config['DBPort'])
        self.dbclient = MongoClient("mongodb://%s:%s@%s:%s" % (self.username, self.password, self.host, self.port))

    async def init_database(self, ctx, embed):
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
        except Exception as e:
            embed.add_field(
                name= '!Failure creating Leveling Database',
                value= f'Die Level Datenbank konnte nicht angelegt werden. \n{e}',
                inline= False
            )
        finally:
            return embed

    @commands.command(name='check_database')
    @commands.has_role(needed_role['maintananceRole'])
    async def check_database(self, ctx):
        dblist = myclient.list_database_names()
        if "skynetdatabase" in dblist:
            print("The database exists.")