import sqlite3, json, os, logging, discord
from discord.utils import get
import os, json, logging
from utils.server.server_utils import create_textchannel as ct
from utils.server.server_utils import create_category as cc
from utils.server.server_utils import set_standard_permission_for_cat

logger = logging.getLogger('SkyNet-Core.Init_Functions')

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../../data/config/config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

async def init_server_sync():

    print('Not implemented yet')

async def init_vote_roles_on(ctx):
    
    guild = ctx.message.author.guild
    place = get(guild.categories, name=maintenance['maintenanceCatName'])
    tc = get(guild.channels, name='rollenverteilung')
    
    lowestrole = get(ctx.guild.roles, name=maintenance['lowestSelfGiveableRole'])
    highestrole = get(ctx.guild.roles, name=maintenance['highestSelfGiveableRole'])

    member = ctx.message.author
    user = member.display_name

    try:
        embed = discord.Embed(
            title='Adding Roles',
            description=f'{user} hat hinzufügen von Rollen ausgelöst.',
            color=discord.Color.dark_gold()
            )

        if not place:
            place, embed = await cc(guild, name=maintenance['maintenanceCatName'], member='Bot', embed=embed)
            embed = await set_standard_permission_for_cat(guild, place, role=guild.default_role, embed=embed)

        if not tc:
            tc, embed = await ct(guild=guild, name=['rollenverteilung'], place=place, embed=embed)

        for role in ctx.guild.roles:
            if role.position < highestrole.position and role.position > lowestrole.position:
                msg = await tc.send(f'Möchtest du die Role {role} haben?')

                await msg.add_reaction(emoji='👍')
                await msg.add_reaction(emoji='👎')
    except Exception as e:
        embed = discord.Embed(
            title='Adding Roles',
            description=f'{user} hat hinzufügen von Rollen ausgelöst.',
            color=discord.Color.dark_gold()
            )

    finally:
        await ctx.message.delete()
        await ctx.send(embed=embed)

async def init_leveling_db(ctx):
    
    guild_id = ctx.message.author.guild.id
    con = sqlite3.connect(f'{source}/../../data/{guild_id}.db')
    cur = con.cursor()
    cur.execute("""Create Table IF NOT EXISTS leveling
    (dc_user_nick text, dc_user_id integer, tw_user_nick text, tw_user_id integer, level integer NOT NULL DEFAULT 1, exp integer NOT NULL DEFAULT 0)""")
    con.commit()
    con.close()

async def init_inter_server_leveling():

    print('Not implemented yet')