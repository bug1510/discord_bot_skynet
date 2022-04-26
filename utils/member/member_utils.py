from discord.utils import get
import logging
import os
import json

logger = logging.getLogger('SkyNet-Core.Member_Utils')

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../../data/config/config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

async def adding_roles(guild, member, roles, embed):

    highestrole = get(guild.roles, name=maintenance['highestSelfGiveableRole'])
    lowestrole = get(guild.roles, name=maintenance['lowestSelfGiveableRole'])

    added_roles = ''
    not_added_roles = ''
    
    try:
        if roles == 'All':
            for role in guild.roles:
                if role.position < highestrole.position and role.position > lowestrole.position:
                    await member.add_roles(role)
                    added_roles += str(role) + '\n'

            embed.add_field(
                name=f'@{member}´s neue Rollen',
                value=added_roles,
                inline=False
                )
                
        elif roles.find(",") > 0:
            para = roles.split(",")
        else:
            para = [roles]

        for e in para:
            role = get(member.guild.roles, name=e)
            # prüfe ob die gewünschte Rolle in der hirarchie höher oder niedriger liegt als die erlaubte
            if role.position < highestrole.position and role.position > lowestrole.position:
                await member.add_roles(role)
                
                embed.add_field(
                    name='!Success adding roles!',
                    value=added_roles
                    )
                
                logger.info(f'{member} hat die Rolle {role} zugewiesen bekommen')
            else:
                
                embed.add_field(
                    name='!Error adding Roles!',
                    value=not_added_roles
                    )
                logger.warning(f'{member} hat versucht eine Rolle zu bekommen die nicht gemanagt ist.')
    except Exception as e:
        logger.warning(f'While adding roles to {member} went something wrong: {e}.')
        embed.add_field(
            name= '!Failure adding Roles',
            value= f'Beim hinzufügen der Rollen ist etwas schief gegangen,\nüberprüfe bitte deine Eingabe.',
            inline=False
        )
        embed.add_field(
            name='Error',
            value=e
        )
    finally:
        return embed

async def removing_roles(guild, member, roles, embed):

    highestrole = get(guild.roles, name=maintenance['highestSelfGiveableRole'])
    lowestrole = get(guild.roles, name=maintenance['lowestSelfGiveableRole'])

    removed_roles = ''

    try:
        if roles == 'All':
            for role in guild.roles:
                if role.position < highestrole.position and role.position > lowestrole.position:
                    await member.remove_roles(role)
                    removed_roles += str(role) + '\n'

            embed.add_field(
                name=f'@{member}´s entfernte Rollen',
                value=removed_roles,
                inline=False
                )
        
        if roles.find(",") > 0:
            para = roles.split(",")
        else:
            para = [roles]

        for e in para:
            role = get(member.guild.roles, name=e)
            if role.position < highestrole.position and role.position > lowestrole.position:
                await member.remove_roles(role)
                
                embed.add_field(
                    name='!Success removing roles!',
                    value=removed_roles
                    )
                
                logger.info(f'{member} hat die Rolle {role} entfernt bekommen')

    except Exception as e:
        logger.warning(f'While removing roles from {member} went something wrong: {e}.')
        embed.add_field(
            name= '!Failure removing Roles',
            value= f'Beim entfernen der Rollen ist etwas schief gegangen,\nüberprüfe bitte deine Eingabe.',
            inline=False
        )
        embed.add_field(
            name='Error',
            value=e
        )

    finally:
        return embed