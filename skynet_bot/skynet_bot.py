#/usr/bin/python3

import discord, os, sys, getopt
from discord.ext import commands
from utils.file_handler import FileHandlingUtils as fhu

configpath = str(f'{os.path.dirname(os.path.abspath(__file__))}/data/config/')
logpath = str(f'{os.path.dirname(os.path.abspath(__file__))}/logs/')
cogpath = str(f'{os.path.dirname(os.path.abspath(__file__))}/cogs/')
ssdbpath = str(f'{os.path.dirname(os.path.abspath(__file__))}/data/')
token = None

def usage():
    print("""
        SkyNet Bot - have fun to use
        
        usage:

            -h or --help        show this help
            -t or --token       define your application token to run the bot. (required!) 
            -c or --config      define the json configfiles path. (default : ./data/config/)
            -l or --log         define the logpath (default ./logs/)
            -m or --modules     define the path for your modules. (default ./cogs/) 
            -d or --database    define where the Single Server Database ist or shoud be placed. (default ./data/)
        
        example:

            use sbot.json as config and write logfile to /var/log/

            skynet_bot.py -t <your token> -c /home/dev/skynet_bot/skynet_bot.json -l /var/log/

    """)

class SkynetCore(commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)
        self.source = os.path.dirname(os.path.abspath(__file__))
        self.configpath = configpath
        self.logpath = logpath
        self.cogpath = cogpath
        self.ssdbpath = ssdbpath

    async def on_ready(self):
        await client.load_extension('cogs.bot.init_bot_functions')
        init_bot_functions = self.get_cog('InitBotFunctions')
        self.loaded_cogs = ['cogs.bot.init_bot_functions']
        
        await init_bot_functions.init_logger()

        self.configpath = configpath
        self.logger.info(f'Core | the configpath was set to: {self.configpath}')
        self.config = fhu.json_handler(path=configpath, filename=str('config.json'))
        self.community_settings = self.config['CommunitySettings']
        self.server_settings = self.config['ServerSettings']
        self.permission_settings = self.config['PermissionSettings']

        await init_bot_functions.init_cogs()

        await init_bot_functions.init_database_handler()


        await client.change_presence(activity=discord.Activity(name='!help', type=2))
        self.logger.info('Core | Client presence was changed')

        self.logger.info('Core | Bot has finished the startup process')
        self.logger.info('Core | Bot was initiated successfully')
        print('Core | Bot was initiated successfully')

if __name__ == '__main__':

    #parameters for bot start
    try:
        opts, args = getopt.getopt(sys.argv[1:],'t:c:l:m:d:h',['token','config','log','modules','database','help'])
    except:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-t', '--token'):
            token = arg
        elif opt in ('-c','--config'):
            configpath = arg
        elif opt in ('-l','--log'):
            logpath = arg
        elif opt in ('-m', '--modules'):
            cogpath = arg
        elif opt in ('-d', '--database'):
            ssdbpath = arg
        elif opt in ('-h','--help'):
            usage()
            sys.exit(1)
        else:
            usage()
            sys.exit(2)

    if not token:
        print('Please enter token')
        usage()
        sys.exit(2)

    intents = discord.Intents.all()

    client = SkynetCore(command_prefix='!',
    description='SKYNET BOT CORE ' + '| V/ 0.8 - ALPHA',
    help_command = commands.DefaultHelpCommand(no_category = 'Help'),
    intents=intents)

    client.run(token)