import logging
from discord.ext import commands

class RoleManagingUtils(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger('SkyNet-Core.Role_Managing_Utils')
    
    async def create_role(self, space):
        try:
            space.role = space.guild.create_role(name=space.name)
            self.logger.info(f'{space.member} created role {space.name} successfully')
            space.embed.add_field(
                name= '!Success creating Role!',
                value= f'Die Rolle {space.role} wurde erstellt.',
                inline=False
            )
            return space

        except Exception as e:
            self.logger.info(f'{space.member} tried to create role {space.name} but it failed due to an error: {e}')
            space.embed.add_field(
                name= '!Failure creating Category connected Role!',
                value= f'Die Rolle {space.name} wurde nicht erstellt,\n{e}.',
                inline=False
            )
            return space

    async def delete_role(self, space):
        try:
            space.role.delete(reason=None)

            self.logger.info(f'{space.member} deleted the role {space.role} successfully')
            embed = embed.add_field(
                name= '!Success deleting Role!',
                value= f'Die Rolle {space.role} wurde gelöscht.',
                inline=False
            )
        except Exception as e:
            self.logger.warning(f'{space.member} tried to delete the role {space.role} but it failed due to an error: {e}')
            embed = embed.add_field(
                name= '!Failure deleting Role!',
                value= f'Beim löschen der Rolle {space.role} ist etwas schief gelaufen,\n{e}.',
                inline=False
            )
        finally:
            return space

async def setup(bot):
    await bot.add_cog(RoleManagingUtils(bot))