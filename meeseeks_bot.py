#!/usr/bin/env python3

import json
import discord
import os
from datetime import datetime
from discord.ext import commands
from discord.utils import get

today = datetime.now()
today = today.strftime("%Y%m%d")
source = os.path.dirname(os.path.abspath(__file__))

# Das ist die finale Struktur des Meeseeks_Bots und damit Version 1.0

initial_extensions = ['cogs.admin', 'cogs.members', 'cogs.simple']

client = commands.Bot(command_prefix='!', description='Meeseeks Bot | V0.6.1')

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

@client.event
async def on_ready():

    await client.change_presence(activity=discord.Activity(name='!help', type=2))
    print('Ich bin bereit')


maintenance = open(source + '/../token.json',)
secret = json.load(maintenance)

client.run(secret['token'])

maintenance.close()