#/usr/bin/python3

from logging.handlers import TimedRotatingFileHandler
import discord, os, sys, getopt, logging
from discord.ext import commands
from datetime import datetime
from utils.config_handler import ConfigHandlingUtils as cohu

token = cohu().json_handler(filename=str('token.json'))

configpath = '/../../data/config/'
logpath = '/../../logs'
class SkynetCore(commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)
        self.today = datetime.now()
        self.today = self.today.strftime("%Y%m%d")
        self.source = os.path.dirname(os.path.abspath(__file__))
        self.config = cohu().json_handler(filename=str('config.json'))
        self.logpath = logpath
        self.configpath = configpath

    async def on_ready(self):
        # await self.init_logger()
        await client.load_extension('cogs.bot.cog_handler')
        cog_handler = self.get_cog('CogHandler')
        await cog_handler.init_cogs(path='/cogs/bot/', file_prefix='cogs.bot.')
        await cog_handler.init_cogs(path='/cogs/server/', file_prefix='cogs.server.')
        await cog_handler.init_cogs(path='/cogs/commands/', file_prefix='cogs.commands.')
        await cog_handler.init_cogs(path='/cogs/member/', file_prefix='cogs.member.')
        await cog_handler.init_cogs(path='/cogs/leveling/', file_prefix='cogs.leveling.')
        await client.change_presence(activity=discord.Activity(name='!help', type=2))
        # self.logger.info('bot started')
        # self.logger.info(f'config file : {self.configpath}')
        # self.logger.info(f'log path : {self.logpath}')
        print('initiated')


    def usage():
        print("""
            SkyNet Bot - have fun to use
            
            usage:

                -h or --help    show this help
                -c or --config  define the json configfiles path      (default : ./../../data/config/)
                -l or --log     define the logpath              (default ./../../logs/)

            example:

                use sbot.json as config and write logfile to /var/log/

                skynet_bot.py -c /home/dev/document/sbot.json -l /var/log/

        """)

    #parameters for bot start
    try:
        opts, args = getopt.getopt(sys.argv[1:],'c:l:h',['config','log','help'])
    except:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h','--help'):
            usage()
            sys.exit(1)
        elif opt in ('-c','--config'):
            config_file = arg
        elif opt in ('-l','--log'):
            logpath = arg
        else:
            usage()
            sys.exit(2)



if __name__ == '__main__':
    intents = discord.Intents.all()

    client = SkynetCore(command_prefix='!',
    description='SKYNET BOT CORE ' + '| V/ 0.8 - ALPHA',
    help_command = commands.DefaultHelpCommand(no_category = 'Help'),
    intents=intents)

    client.run(token['token'])