import json, os, logging
from discord.utils import get
from utils.server.server_utils import create_textchannel as ct
from utils.server.server_utils import create_category as cc
from utils.server.server_utils import set_standard_permission_for_cat
from data.config.db_secret import myclient

logger = logging.getLogger('SkyNet-Core.Init_Functions')

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../../data/config/config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

async def init_server_sync(ctx, embed):

    embed.add_field(
    name= '!Information on Multi-Server-Sync!',
    value= 'Multi-Server-Sync is not implemented yet',
    inline= False
)

    return embed

async def init_vote_roles_on(ctx, embed):
    
    guild = ctx.message.author.guild
    place = get(guild.categories, name=maintenance['maintenanceCatName'])
    tc = get(guild.channels, name='rollenverteilung')
    
    lowestrole = get(ctx.guild.roles, name=maintenance['lowestSelfGiveableRole'])
    highestrole = get(ctx.guild.roles, name=maintenance['highestSelfGiveableRole'])

    if not place:
        place, embed = await cc(guild, name=maintenance['maintenanceCatName'], member='Bot', embed=embed)
        embed = await set_standard_permission_for_cat(guild, place, role=guild.default_role, embed=embed)

    if not tc:
        tc, embed = await ct(guild=guild, name=['rollenverteilung'], place=place, embed=embed)
    try:
        for role in ctx.guild.roles:
            if role.position < highestrole.position and role.position > lowestrole.position:
                msg = await tc.send(f'Möchtest du die Role {role} haben?')

                await msg.add_reaction(emoji='👍')
                await msg.add_reaction(emoji='👎')
    
        embed.add_field(
            name= '!Success creating Roles on Vote!',
            value= 'Die Vote Nachrichten wurden angelegt.',
            inline= False
        )

    except Exception as e:
        embed.add_field(
            name= '!Failure creating Roles on Vote!',
            value= f'Die Vote Nachrichten konnten nicht angelegt werden. \n{e}',
            inline= False
        )
    finally:
        return embed

async def init_database(ctx, embed):
    
    guild_id = ctx.message.author.guild.id

    try:

        with open(config_file) as f:
            data = json.load(f)

        mydb = myclient[str(guild_id)]

        mycol = mydb["serverconfig"]

        mycol.insert_one(data)

        for y in mycol.find():
            print(y) 

        embed.add_field(
            name= '!Success creating Leveling Database!',
            value= 'Die Level Datenbank wurde angelegt.',
            inline= False
        )

    except Exception as e:
        embed.add_field(
            name= '!Failure creating Leveling Database',
            value= f'Die Level Datenbank konnte nicht angelegt werden. \n{e}',
            inline= False
        )

    finally:
        return embed

async def init_inter_server_leveling(ctx, embed):

    embed.add_field(
    name= '!Information Inter-Server-Leveling!',
    value= 'Inter-Server-Leveling is not implemented yet',
    inline= False
)

    return embed