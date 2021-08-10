import logging,os
import discord
from discord.ext import commands
source = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)
class BotManaging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='list')
    @commands.has_role('El-Special')
    async def list_cog(self, context):
        """ list all cogs on server"""
        ListRolesField = ''
        try:
            for CogFile in os.listdir(source):
                if CogFile.endswith('.py') and CogFile != 'bot-managing.py':
                    ListRolesField += '* ' + str(CogFile[:-3]) + '\n'
        except:
            logger.warning('could not list cogs')
        
        embed = discord.Embed(title='List Roles',
                              description=ListRolesField,
                              color=discord.Color.orange())
        await context.send(embed=embed)


    @commands.command(name='load')
    @commands.has_role('El-Special')
    async def load_cog(self, context, extension):
        """verbindet ein noch nicht geladenes Modul um ein neustart des Bots zu vermeiden."""
        extension_path = 'cogs.' + extension
        member = context.message.author
        mbed = discord.Embed(title='Load erfolgreich', description=f'Das Modul "{extension}" ist nun benutzbar.')

        try:
            self.bot.load_extension(extension_path)
            await context.send(embed=mbed)
            logger.info('cog ' + extension + ' loaded by ' + str(member))
        except:
            await context.send('Das angegebene Modul ' + extension + ' existiert nicht, oder hat einen anderen Namen.')
            logger.warning(str(member) + ' tried to load the cog ' + extension + ' and it could not be loaded')
            pass

    @commands.command(name='unload')
    @commands.has_role('El-Special')
    async def unload_cog(self, context, extension):
        """trennt ein laufendes Modul um es ohne Impact berabeiten oder entfernen zu können."""
        extension_path = 'cogs.' + extension
        member = context.message.author
        mbed = discord.Embed(title='Unload erfolgreich', description=f'Das Modul "{extension}" ist nun nicht mehr benutzbar.')

        if extension == 'bot-managing':
            await context.send('Dies ist eine Anti-Lockout-Rule um die Grundfunktionen des Bots zu schützen.')
            logger.critical(str(member) + ' tried to unload the cog ' + extension + ' that shouldnt be unloaded')
        else:
            try:
                self.bot.unload_extension(extension_path)
                await context.send(embed=mbed)
                logger.info('cog ' + extension + ' unloaded by ' + str(member))
            except:
                await context.send('Das angegebene Modul ' + extension + ' existiert nicht, oder hat einen anderen Namen.')
                logger.warning(str(member) + ' tried to unload the cog ' + extension + ' and it could not be unloaded')

    @commands.command(name='reload')
    @commands.has_role('El-Special')
    async def reload_cog(self, context, extension):
        """lädt ein Modul neu wenn es sich geändert haben sollte."""
        extension_path = 'cogs.' + extension
        member = context.message.author
        mbed = discord.Embed(title='Reload erfolgreich', description=f'Das Modul "{extension}" ist nun wieder benutzbar.')

        try:
            self.bot.reload_extension(extension_path)
            await context.send(embed=mbed)
            logger.info('cog ' + extension + ' reloaded by ' + str(member))
        except:
            await context.send('Das angegebene Modul ' + extension + ' existiert nicht, oder hat einen anderen Namen.')
            logger.warning(str(member) + ' tried to reload the cog ' + extension + ' and it could not be reloaded')

def setup(bot):
    bot.add_cog(BotManaging(bot))