#/usr/bin/python3

from logging.handlers import TimedRotatingFileHandler
import discord, os, sys, getopt, logging
from discord.ext import commands
from datetime import datetime
from utils.bot.config_handler import ConfigHandlingUtils as cohu

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

    async def init_logger(self):
        #logging
        #check log folder

        if not os.path.exists(self.logpath):
            os.makedirs(self.logpath)

        self.logger = logging.getLogger('SkyNet-Core')
        self.logger.setLevel(logging.INFO)

        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s | %(message)s')

        rotatinglogs = TimedRotatingFileHandler(
            filename=self.logpath + '/skynet_bot.log',
            when="midnight",
            interval=1,
            backupCount=5
            )
        rotatinglogs.setLevel(logging.INFO)
        rotatinglogs.setFormatter(format)

        self.logger.addHandler(rotatinglogs)


    async def init_modules(self, initial_extension=['cogs.bot']): #self.config['modules']):
        #this loop collects all modules in cogs and put them in initial_extension
        for CogFile in os.listdir(self.source + '/cogs/'):
            if CogFile.endswith('.py'):
                module = 'cogs.' + CogFile[:-3]
                if module not in initial_extension:
                    initial_extension.append(module)
                    self.logger.info('append cog - ' + module)

        #this loop loads the extension in the bot
        for extension in initial_extension:
            try:
                client.load_extension(extension)
            except Exception as e:
                print(e)

    async def on_ready(self):
        await self.init_logger()
        await self.init_modules()
        await client.change_presence(activity=discord.Activity(name='!help', type=2))
        self.logger.info('bot started')
        self.logger.info(f'config file : {self.configpath}')
        self.logger.info(f'log path : {self.logpath}')
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
    intents = discord.Intents.default()
    intents.members = True

    client = SkynetCore(command_prefix='!',
    description='SKYNET BOT CORE ' + '| V/ 0.8 - ALPHA',
    help_command = commands.DefaultHelpCommand(no_category = 'Help'),
    intents=intents)

    client.run(token['token'])