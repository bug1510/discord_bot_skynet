import sqlite3, json, os, logging
from discord.utils import get
import os, json, logging
from datetime import datetime

today = datetime.now()
today = today.strftime("%Y%m%d")
source = os.path.dirname(os.path.abspath(__file__))
logpath = source + '/logs/'
config_file = source + '/data/config/config.json'

conf = open(config_file, "r")
maintenance = json.load(conf)
conf.close()

logger = logging.getLogger('SkyNet-Core.Init_Functions')

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../data/config/config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

async def init_vote_roles_on(ctx):
    
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

async def init_leveling_db(ctx):
    
    guild_id = ctx.message.author.guild.id
    con = sqlite3.connect(f'{source}/../../data/{guild_id}.db')
    cur = con.cursor()
    cur.execute("""Create Table IF NOT EXISTS leveling
    (dc_user_nick text, dc_user_id integer, tw_user_nick text, tw_user_id integer, level integer NOT NULL DEFAULT 1, exp integer NOT NULL DEFAULT 0)""")
    con.commit()
    con.close()