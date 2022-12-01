import logging
from discord.utils import get
from utils.bot.config_handler import ConfigHandlingUtils as cohu

class RoleHandlingUtils():
    def __init__(self) -> None:
        self.logger = logging.getLogger('SkyNet-Core.Role_Handling_Utils')
        self.config = cohu().json_handler(filename=str('config.json'))
    
    async def adding_roles(self, guild, member, roles, embed):

        highestrole = get(guild.roles, name=self.config['highestSelfGiveableRole'])
        lowestrole = get(guild.roles, name=self.config['lowestSelfGiveableRole'])

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
                    
                    added_roles = role

                    embed.add_field(
                        name='!Success adding roles!',
                        value=added_roles
                        )
                    
                    self.logger.info(f'{member} hat die Rolle {role} zugewiesen bekommen')
                else:
                    
                    not_added_roles = role

                    embed.add_field(
                        name='!Error adding Roles!',
                        value=not_added_roles
                        )
                    self.logger.warning(f'{member} hat versucht eine Rolle zu bekommen die nicht gemanagt ist.')
        except Exception as e:
            self.logger.warning(f'While adding roles to {member} went something wrong: {e}.')
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

    async def removing_roles(self, guild, member, roles, embed):

        highestrole = get(guild.roles, name=self.config['highestSelfGiveableRole'])
        lowestrole = get(guild.roles, name=self.config['lowestSelfGiveableRole'])

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
                    
                    self.logger.info(f'{member} hat die Rolle {role} entfernt bekommen')

        except Exception as e:
            self.logger.warning(f'While removing roles from {member} went something wrong: {e}.')
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