import sqlite3, json, os, logging
from discord.utils import get

from logging.handlers import TimedRotatingFileHandler
import discord, os, json, sys, getopt, logging
from discord.ext import commands
from datetime import datetime

today = datetime.now()
today = today.strftime("%Y%m%d")
source = os.path.dirname(os.path.abspath(__file__))
logpath = source + '/logs/'
config_file = source + '/data/config/config.json'

conf = open(config_file, "r")
maintenance = json.load(conf)
conf.close()

logger = logging.getLogger('SkyNet-Core.CommunityCommands')

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../data/config/config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

async def init_logger(self):
    # logging
    ## check log folder

    if not os.path.exists(logpath):
        os.makedirs(logpath)

    self.logger = logging.getLogger('SkyNet-Core')
    self.logger.setLevel(logging.INFO)

    format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s | %(message)s')

    rotatinglogs = TimedRotatingFileHandler(
        filename=logpath + '/skynet_bot.log',
        when="midnight",
        interval=1,
        backupCount=5
        )
    rotatinglogs.setLevel(logging.INFO)
    rotatinglogs.setFormatter(format)

    self.logger.addHandler(rotatinglogs)

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

async def init_vote_roles_on(self, ctx):
    guild = ctx.message.author.guild
    channel = get(guild.channels, name='rollenverteilung')
    lowest = get(ctx.guild.roles, name='@everyone')
    highestrole = get(ctx.guild.roles, name=maintenance['highestSelfGiveableRole'])
    streamin_grole = get(guild.roles, name='Streamer:in')

    if not channel:
        channel = await guild.create_text_channel(name='rollenverteilung')

    for role in ctx.guild.roles:
        if role.position < highestrole.position and role.position > lowest.position:
            if role == streamin_grole:
                await channel.send('Bist du ein Streamer oder eine Streamerin ?')
            else:
                await channel.send(f'Spielst du {role} ?')

    await ctx.message.delete()

async def init_leveling_db():
    '''Initialisiert das Leveling auf deinem Server. Also viel Spaß!'''
    guild_id = ctx.message.author.guild.id
    con = sqlite3.connect(f'{source}/../../data/{guild_id}.db')
    cur = con.cursor()
    cur.execute("""Create Table IF NOT EXISTS leveling
    (dc_user_nick text, dc_user_id integer, tw_user_nick text, tw_user_id integer, level integer NOT NULL DEFAULT 1, exp integer NOT NULL DEFAULT 0)""")
    con.commit()
    con.close()