import discord
from discord.ext import commands
from discord.utils import get
from utils.file_handler import FileHandlingUtils as fhu
from utils.custom_object import CustomObject

class RoleHandler(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def checking_role(self, guild, role):
        highestrole = get(guild.roles, name=self.bot.config['highestSelfGiveableRole'])
        lowestrole = get(guild.roles, name=self.bot.config['lowestSelfGiveableRole'])
        try:
            if role.position < highestrole.position and role.position > lowestrole.position:
                return True
        except Exception as e:
            self.bot.logger.warning(f'RoleHandler | checking the Role {role} failed due to: {e}')

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

    async def adding_roles(self, customobject:CustomObject) -> CustomObject:
        for r in customobject.roles:
                try:
                    await customobject.member.add_roles(customobject.roles)
                    self.bot.logger.info(f'RoleHandler | {customobject.member} was given the Role: {r}')
                    customobject.embed.add_field(name=f'Success adding role!', value=r, inline=False)
                except Exception as e:
                    self.logger.warning(f'RoleHandler | While adding role {r} to {customobject.member} went something wrong: {e}.')
                    customobject.embed.add_field(
                        name= '!Failure adding Roles',
                        value= f'Beim hinzufügen der Rollen ist etwas schief gegangen,\nüberprüfe bitte deine Eingabe.',
                        inline=False
                    )
                    customobject.embed.add_field(name='Error', value=e)
                    customobject.embed.color = discord.Color.red()
        return customobject

    async def removing_roles(self, customobject: CustomObject) -> CustomObject:
        for r in customobject.roles:
            try:
                await customobject.member.remove_roles(r)
                self.bot.logger.info(f'RoleHandler | Removed {r} from {customobject.member}.')
                customobject.embed.add_field(name=f'Success removing role!', value=r, inline=False)
            except Exception as e:
                self.bot.logger.warning(f'RoleHandler | While removing roles from {customobject.member} went something wrong: {e}.')
                customobject.embed.add_field(
                    name= '!Failure removing Roles',
                    value= f'Beim entfernen der Rollen ist etwas schief gegangen,\nüberprüfe bitte deine Eingabe.',
                    inline=False
                )
                customobject.embed.add_field(name='Error', value=e)
                customobject.embed.color = discord.Color.red()
        return customobject       
        
async def setup(bot):
    await bot.add_cog(RoleHandler(bot))