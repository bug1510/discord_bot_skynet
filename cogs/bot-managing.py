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
        ListModulesField = ''
        try:
            for CogFile in os.listdir(source):
                if CogFile.endswith('.py') and CogFile != 'bot-managing.py':
                    ListModulesField += '* ' + str(CogFile[:-3]) + '\n'
        except:
            logger.warning('could not list cogs')
        
        embed = discord.Embed(title='List of Modules',
                              description=ListModulesField,
                              color=discord.Color.blue())
        await context.send(embed=embed)


    @commands.command(name='load')
    @commands.has_role('El-Special')
    async def load_cog(self, context, extension):
        """verbindet ein noch nicht geladenes Modul um ein neustart des Bots zu vermeiden."""
        extension_path = 'cogs.' + extension
        member = context.message.author
        smbed = discord.Embed(title='Load erfolgreich', description=f'Das Modul "{extension}" ist nun benutzbar.', color=discord.Color.green())
        fmbed = discord.Embed(title='Load fehlgeschlagen', description=f'Das Modul "{extension}" existiert nicht oder ist falsch geschrieben.', color=discord.Color.red())

        try:
            self.bot.load_extension(extension_path)
            await context.send(embed=smbed)
            logger.info('cog ' + extension + ' loaded by ' + str(member))
        except:
            await context.send(embed=fmbed)
            logger.warning(str(member) + ' tried to load the cog ' + extension + ' and it could not be loaded')
            pass

    @commands.command(name='unload')
    @commands.has_role('El-Special')
    async def unload_cog(self, context, extension):
        """trennt ein laufendes Modul um es ohne Impact berabeiten oder entfernen zu können."""
        extension_path = 'cogs.' + extension
        member = context.message.author
        smbed = discord.Embed(title='Unload erfolgreich', description=f'Das Modul "{extension}" ist nun nicht mehr benutzbar.', color=discord.Color.green())
        fmbed = discord.Embed(title='Unload fehlgeschlagen', description=f'Das Modul "{extension}" existiert nicht oder ist falsch geschrieben.', color=discord.Color.red())
        wmbed = discord.Embed(title='Dein Ernst?', description='Dies ist eine Anti-Lockout-Rule um die Grundfunktionen des Bots zu schützen.', color=discord.Color.orange())

        if extension == 'bot-managing':
            await context.send(embed=wmbed)
            logger.critical(str(member) + ' tried to unload the cog ' + extension + ' that shouldnt be unloaded')
        else:
            try:
                self.bot.unload_extension(extension_path)
                await context.send(embed=smbed)
                logger.info('cog ' + extension + ' unloaded by ' + str(member))
            except:
                await context.send(embed=fmbed)
                logger.warning(str(member) + ' tried to unload the cog ' + extension + ' and it could not be unloaded')

    @commands.command(name='reload')
    @commands.has_role('El-Special')
    async def reload_cog(self, context, extension):
        """lädt ein Modul neu wenn es sich geändert haben sollte."""
        extension_path = 'cogs.' + extension
        member = context.message.author
        smbed = discord.Embed(title='Reload erfolgreich', description=f'Das Modul "{extension}" ist nun wieder benutzbar.', color=discord.Color.green())
        fmbed = discord.Embed(title='Reload fehlgeschlagen', description=f'Das Modul "{extension}" existiert nicht oder ist falsch geschrieben.', color=discord.Color.red())

        try:
            self.bot.reload_extension(extension_path)
            await context.send(embed=smbed)
            logger.info('cog ' + extension + ' reloaded by ' + str(member))
        except:
            await context.send(embed=fmbed)
            logger.warning(str(member) + ' tried to reload the cog ' + extension + ' and it could not be reloaded')

def setup(bot):
    bot.add_cog(BotManaging(bot))