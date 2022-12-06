import discord
from discord.ext import commands
from utils.custom_object import CustomObject

class RoleManagingUtils(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    async def create_role(self, customobject:CustomObject) -> CustomObject:
        try:
            customobject.role = customobject.guild.create_role(name=customobject.name)
            self.bot.logger.info(f'RoleManagingUtils | created role {customobject.name} successfully')
            customobject.embed.add_field(
                name= '!Success creating Role!',
                value= f'Die Rolle {customobject.role} wurde erstellt.',
                inline=False
            )
        except Exception as e:
            self.bot.logger.critical(f'RoleManagingUtils | tried to create role {customobject.name} but it failed due to an error: {e}')
            customobject.embed.add_field(
                name= '!Failure creating Category connected Role!',
                value= f'Die Rolle {customobject.name} wurde nicht erstellt,\nüberprüfe bitte deine Server Konfiguration und Logs.',
                inline=False
            )
            customobject.embed.color = discord.Color.red()
        finally:
            return customobject

    async def delete_role(self, customobject:CustomObject) -> CustomObject:
        try:
            customobject.role.delete(reason=None)

            self.bot.logger.info(f'RoleManagingUtils | deleted the role {customobject.role} successfully')
            customobject.embed.add_field(
                name= '!Success deleting Role!',
                value= f'Die Rolle {customobject.role} wurde gelöscht.',
                inline=False
            )
        except Exception as e:
            self.bot.logger.critical(f'RoleManagingUtils | tried to delete the role {customobject.role} but it failed due to an error: {e}')
            customobject.embed.add_field(
                name= '!Failure deleting Role!',
                value= f'Beim löschen der Rolle {customobject.role} ist etwas schief gelaufen,\nüberprüfe bitte deine Server Konfiguration und Logs.',
                inline=False
            )
            customobject.embed.color = discord.Color.red()
        finally:
            return customobject

async def setup(bot):
    await bot.add_cog(RoleManagingUtils(bot))