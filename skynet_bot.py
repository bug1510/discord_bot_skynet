#!/usr/bin/python3

from logging.handlers import TimedRotatingFileHandler
import discord, os, json, sys, getopt, logging
from discord.ext import commands
from datetime import datetime
import utils.bot.init_functions as inf
today = datetime.now()
today = today.strftime("%Y%m%d")
source = os.path.dirname(os.path.abspath(__file__))
logpath = source + '/logs/'
config_file = source + '/data/config/config.json'

conf = open(config_file, "r")
maintenance = json.load(conf)
conf.close()

intents = discord.Intents.default()
intents.members = True

class SkynetCore(commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)

    async def on_ready(self):
        self.logger = await inf.init_logger()
        await self.init_modules()
        await client.change_presence(activity=discord.Activity(name='!help', type=2))
        self.logger.info('bot started')
        self.logger.info('config file : ' + config_file)
        self.logger.info('log path : ' + logpath)
        print('initiated')

    def usage():
        print("""
            SkyNet Bot - have fun to use
            
            usage:

                -h or --help    show this help
                -c or --config  define the json configfile      (default : ./token.json)
                -l or --log     define the logpath              (default ./logs/)

            example:

                use sbot.json as config and write logfile to /var/log/

                skynet_bot.py -c /home/dev/document/sbot.json -l /var/log/

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

client = SkynetCore(command_prefix='!', 
description=maintenance['botName'] + maintenance['version'],
help_command = commands.DefaultHelpCommand(no_category = 'Help'),
intents=intents
)

if __name__ == '__main__':
    client.run(maintenance['token'])