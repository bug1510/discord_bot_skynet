#/usr/bin/python3

import discord, os, sys, getopt
from discord.ext import commands
from utils.file_handler import FileHandlingUtils as fhu

configpath = str(f'{os.path.dirname(os.path.abspath(__file__))}/data/config/')
logpath = str(f'{os.path.dirname(os.path.abspath(__file__))}/logs/')
cogpath = str(f'{os.path.dirname(os.path.abspath(__file__))}/cogs/')
ssdbpath = str(f'{os.path.dirname(os.path.abspath(__file__))}/data/')

class SkynetCore(commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)
        self.source = os.path.dirname(os.path.abspath(__file__))

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


    def usage():
        print("""
            SkyNet Bot - have fun to use
            
            usage:

                -h or --help    show this help
                -c or --config  define the json configfiles path      (default : ./data/config/)
                -l or --log     define the logpath              (default ./logs/)

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

    client.run((fhu.json_handler(path=configpath, filename=str('token.json')))['token'])