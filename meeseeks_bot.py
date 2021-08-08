#!/usr/bin/env python3

import json
import os
import logging
from datetime import datetime
import discord
from discord.ext import commands
from discord.utils import get

today = datetime.now()
today = today.strftime("%Y%m%d")
source = os.path.dirname(os.path.abspath(__file__))
Version = '0.7 - ALPHA'
logpath = source + '/logs/'

# logging

# check log folder 
if not os.path.exists(logpath):
    os.makedirs(logpath)

logging.basicConfig(
    filename= logpath + str(today) + '_discord_bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s | %(message)s',
    level=logging.INFO
    )

logger = logging.getLogger(__name__)

# Das ist die finale Struktur des Meeseeks_Bots und damit Version 1.0

initial_extensions = [
    'cogs.admin',
    'cogs.members',
    'cogs.simple'
    ]

for CogFile in os.listdir(source + '/cogs/'):
    if CogFile.endswith('.py'):
        module = 'cogs.' + CogFile[:-3]
        if module not in initial_extensions:
            initial_extensions.append(module)
            logger.info('append cog - ' + module)

# change no category in !help
help_command = commands.DefaultHelpCommand(no_category = 'Commands')

client = commands.Bot(
    command_prefix='?',
    description='Meeseeks Bot | V' + Version,
    help_command = help_command
    )

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            client.load_extension(extension)
            logger.info('cog ' + module + ' loaded')
        except:
            logger.warn('cog ' + module + ' could not be loaded')
            pass

@client.event
async def on_ready():

    await client.change_presence(activity=discord.Activity(name='?help', type=2))
    print('Ich bin bereit')
    logger.info('bot started')

maintenance = open(source + '/token.json')
secret = json.load(maintenance)

client.run(secret['token'])

maintenance.close()