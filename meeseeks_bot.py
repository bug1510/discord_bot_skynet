import discord, os, json, sys, getopt, logging
from discord.ext import commands
from datetime import datetime

today = datetime.now()
today = today.strftime("%Y%m%d")
source = os.path.dirname(os.path.abspath(__file__))
logpath = source + '/logs/'
config_file = source + '/config.json'

conf = open(config_file, "r")
maintenance = json.load(conf)
conf.close()

#check your config.json file for standard entries
initial_extension = maintenance['modules']

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

class MeeseeksCore(commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)

    async def init_logger(self):
        # logging
        ## check log folder 
        if not os.path.exists(logpath):
            os.makedirs(logpath)
        logging.basicConfig(
            filename= logpath + '/' + str(today) + '_discord_bot.log',
            format='%(asctime)s - %(name)s - %(levelname)s | %(message)s',
            level=logging.INFO
            )
        self.logger = logging.getLogger(__name__)

    async def init_modules(self):
        #this loop collects all modules in cogs and put them in initial_extension
        for CogFile in os.listdir(source + '/cogs/'):
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
        self.logger.info('config file : ' + config_file)
        self.logger.info('log path : ' + logpath)
        print('initiated')

    def usage():
        print("""
            Meeseeks Bot - have fun to use
            
            usage:

                -h or --help    show this help
                -c or --config  define the json configfile      (default : ./token.json)
                -l or --log     define the logpath              (default ./logs/)

            example:

                use mbot.json as config and write logfile to /var/log/

                meeseeks_bot.py -c /home/dev/document/mbot.json -l /var/log/

        """)

    # parameters for bot start
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

client = MeeseeksCore(command_prefix='!', description=maintenance['botName'] + maintenance['version'], help_command = commands.DefaultHelpCommand(no_category = 'Help'))

if __name__ == '__main__':
    client.run(maintenance['token'])