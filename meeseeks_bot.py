#!/usr/bin/env python3

import json
import os,sys,getopt
import logging
from datetime import datetime
import discord
from discord.ext import commands
from discord.utils import get

today = datetime.now()
today = today.strftime("%Y%m%d")
source = os.path.dirname(os.path.abspath(__file__))
Version = '0.6.3 - ALPHA'
BotName = 'Meeseeks Bot | V' + Version
logpath = source + '/logs/'
config_file = source + '/token.json'


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

# logging

## check log folder 
if not os.path.exists(logpath):
    os.makedirs(logpath)
logging.basicConfig(
    filename= logpath + '/' + str(today) + '_discord_bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s | %(message)s',
    level=logging.INFO
    )
logger = logging.getLogger(__name__)

# Das ist die finale Struktur des Meeseeks_Bots

initial_extension = ['cogs.bot-managing']

for CogFile in os.listdir(source + '/cogs/'):
    if CogFile.endswith('.py'):
        module = 'cogs.' + CogFile[:-3]
        if module not in initial_extension:
            initial_extension.append(module)
            logger.info('append cog - ' + module)

# change no category in !help
help_command = commands.DefaultHelpCommand(no_category = 'Commands')

client = commands.Bot(
    command_prefix='!',
    description='Meeseeks Bot | V' + Version,
    help_command = help_command
    )

if __name__ == '__main__':
    for extension in initial_extension:
        try:
            client.load_extension(extension)
            logger.info('cog ' + extension + ' loaded')
        except:
            logger.warning('cog ' + extension + ' could not be loaded')
            pass

@client.event
async def on_ready():

    await client.change_presence(activity=discord.Activity(name='!help', type=2))
    print('Ich bin bereit')
    logger.info('bot started')
    logger.info('config file : ' + config_file)
    logger.info('log path : ' + logpath)

maintenance = open(config_file)
secret = json.load(maintenance)

client.run(secret['token'])

maintenance.close()