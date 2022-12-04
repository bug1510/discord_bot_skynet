import discord
from discord.ext import commands
from discord.utils import get
from utils.file_handler import FileHandlingUtils as fhu
from utils.custom_objects import Space

class RoleHandler(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def checking_role(self, guild, role):
        highestrole = get(guild.roles, name=self.bot.config['highestSelfGiveableRole'])
        lowestrole = get(guild.roles, name=self.bot.config['lowestSelfGiveableRole'])

        if role.position < highestrole.position and role.position > lowestrole.position:
            return True

    async def listing_role(self, guild, ListRolesField, embed):
        try:
            for role in guild.roles:
                if (self.check_role(guild=guild, role=role)):
                    ListRolesField += str(role) + '\n'
                else:
                    pass
        except Exception as e:
            self.bot.logger(f'RoleHandler | Listing the Roles failed due to: {e}')
            embed.color = discord.Color.red()
        finally:
            return embed

    async def adding_roles(self, guild, member, roles, embed):
        added_role = ''
        not_added_role = ''
        match roles:
            case 'All':
                try:
                    for role in guild.roles:
                        if (self.check_role(guild=guild, role=role)):
                            await member.add_roles(role)
                            added_role += str(role) + '\n'
                    embed.add_field(name='!Success adding roles!', value=added_role, inline=False)
                    self.bot.logger.info(f'RoleHandler | {member} hat alle Rollen die zur Verfügung stehen zugewiesen bekommen')
                except Exception as e:
                    self.bot.logger.warning(f'RoleHandler | While adding roles to {member} went something wrong: {e}.')
                    embed.add_field(
                        name= '!Failure adding Roles',
                        value= f'Beim hinzufügen der Rollen ist etwas schief gegangen,\nüberprüfe bitte deine Eingabe.',
                        inline=False
                    )
                    embed.add_field(name='Error', value=e)
                    embed.color = discord.Color.red()
                finally:
                    return embed
            case roles.find(","):
                para = roles.split(",")
                try:
                    for p in para:
                        role = get(member.guild.roles, name=p)
                        if (self.check_role(guild=guild, role=role)):
                            await member.add_roles(role)
                            added_role = role
                            self.bot.logger.info(f'RoleHandler | {member} hat die Rolle {role} zugewiesen bekommen')
                        else:
                            not_added_role = role
                            embed.add_field(name='!Error adding Roles!', value=not_added_role)
                            self.bot.logger.warning(f'RoleHandler | {member} hat versucht eine Rolle zu bekommen die nicht gemanagt ist.')
                    embed.add_field(name='!Success adding roles!', value=added_role)
                except Exception as e:
                    self.logger.warning(f'RoleHandler | While adding roles to {member} went something wrong: {e}.')
                    embed.add_field(
                        name= '!Failure adding Roles',
                        value= f'Beim hinzufügen der Rollen ist etwas schief gegangen,\nüberprüfe bitte deine Eingabe.',
                        inline=False
                    )
                    embed.add_field(name='Error', value=e)
                    embed.color = discord.Color.red()
                finally:
                    return embed
            case _:
                try:
                    para = [roles]
                    for e in para:
                        role = get(member.guild.roles, name=e)
                        if (self.check_role(guild=guild, role=role)):
                            await member.add_roles(role)
                            added_roles = role
                            embed.add_field(name='!Success adding roles!', value=added_roles)
                            self.bot.logger.info(f'RoleHandler | {member} hat die Rolle {role} zugewiesen bekommen')
                        else:
                            not_added_roles = role
                            embed.add_field(name='!Error adding Roles!', value=not_added_roles)
                            self.bot.logger.warning(f'RoleHandler | {member} hat versucht eine Rolle zu bekommen die nicht gemanagt ist.')
                except Exception as e:
                    self.bot.logger.warning(f'RoleHandler | While adding roles to {member} went something wrong: {e}.')
                    embed.add_field(
                        name= '!Failure adding Roles',
                        value= f'Beim hinzufügen der Rollen ist etwas schief gegangen,\nüberprüfe bitte deine Eingabe.',
                        inline=False
                    )
                    embed.add_field(name='Error',value=e)
                    embed.color = discord.Color.red()
                finally:
                    return embed

    async def removing_roles(self, guild, member, roles, embed):
        removed_roles = ''
        match roles:
            case 'All':
                try:
                    for role in guild.roles:
                        if (self.check_role(guild=guild, role=role)):
                            await member.remove_roles(role)
                            removed_roles += str(role) + '\n'
                    embed.add_field(name=f'Success removing roles!', value=removed_roles, inline=False)
                except Exception as e:
                    self.bot.logger.warning(f'RoleHandler | While removing roles from {member} went something wrong: {e}.')
                    embed.add_field(
                        name= '!Failure removing Roles',
                        value= f'Beim entfernen der Rollen ist etwas schief gegangen,\nüberprüfe bitte deine Eingabe.',
                        inline=False
                    )
                    embed.add_field(name='Error', value=e)
                finally:
                    return embed
            
            case roles.find(","):
                try:
                    para = roles.split(",")
                    for e in para:
                        role = get(member.guild.roles, name=e)
                        if (self.check_role(guild=guild, role=role)):
                            await member.remove_roles(role)
                            embed.add_field(name='!Success removing roles!', value=removed_roles)
                    self.bot.logger.info(f'RoleHandler | {member} hat die Rolle {role} entfernt bekommen')
                except Exception as e:
                    self.bot.logger.warning(f'RoleHandler | While removing roles from {member} went something wrong: {e}.')
                    embed.add_field(
                        name= '!Failure removing Roles',
                        value= f'Beim entfernen der Rollen ist etwas schief gegangen,\nüberprüfe bitte deine Eingabe.',
                        inline=False
                    )
                    embed.add_field(name='Error', value=e)
                finally:
                    return embed

            case _:
                try:
                    para = [roles]
                    for e in para:
                        role = get(member.guild.roles, name=e)
                        if (self.check_role(guild=guild, role=role)):
                            await member.remove_roles(role)
                            embed.add_field(
                                name='!Success removing roles!',
                                value=removed_roles
                                )
                    self.bot.logger.info(f'RoleHandler | {member} hat die Rolle {role} entfernt bekommen')
                except Exception as e:
                    self.bot.logger.warning(f'RoleHandler | While removing roles from {member} went something wrong: {e}.')
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

async def setup(bot):
    await bot.add_cog(RoleHandler(bot))