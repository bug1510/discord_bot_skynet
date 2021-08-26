import logging, os, json
import discord
from discord.ext import commands
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionFailed, ExtensionNotFound, ExtensionNotLoaded, NoEntryPointError
source = os.path.dirname(os.path.abspath(__file__))

config_file = source + '/../config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

logger = logging.getLogger(__name__)
class BotManaging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='list')
    @commands.has_role(maintenance['maintananceRole'])
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
        await context.message.delete()


    @commands.command(name='load')
    @commands.has_role(maintenance['maintananceRole'])
    async def load_cog(self, context, extension):
        """verbindet ein noch nicht geladenes Modul um ein neustart des Bots zu vermeiden."""
        extension_path = 'cogs.' + extension
        member = context.message.author
        smbed = discord.Embed(title='Load erfolgreich', description=f'Das Modul "{extension}" ist nun benutzbar.', color=discord.Color.green())
        NFmbed = discord.Embed(title='Load fehlgeschlagen', description=f'Das Modul "{extension}" existiert nicht', color=discord.Color.red())
        ALmbed = discord.Embed(title='Load fehlgeschlagen', description=f'Das Modul "{extension}" ist bereits geladen', color=discord.Color.red())
        NEmbed = discord.Embed(title='Load fehlgeschlagen', description=f'Das Modul "{extension}" hat keine Setup Funtion', color=discord.Color.red())
        Fmbed = discord.Embed(title='Load fehlgeschlagen', description=f'Das Modul "{extension}" hatte ein Problem beim ausführen der Setup Funktion', color=discord.Color.red())


        try:
            self.bot.load_extension(extension_path)
            await context.send(embed=smbed)
            logger.info('cog ' + extension + ' loaded by ' + str(member))
        except ExtensionNotFound:
            await context.send(embed=NFmbed)
            logger.warning(str(member) + ' tried to load the cog ' + extension + ' but it doesnt exist')
            pass
        except ExtensionAlreadyLoaded:
            await context.send(embed=ALmbed)
            logger.warning(str(member) + ' tried to load the cog ' + extension + ' but its allready loaded')
            pass
        except NoEntryPointError:
            await context.send(embed=NEmbed)
            logger.warning(str(member) + ' tried to load the cog ' + extension + ' but it has no setup funtion')
            pass
        except ExtensionFailed:
            await context.send(embed=Fmbed)
            logger.warning(str(member) + ' tried to load the cog ' + extension + ' but the setup function had an execution error')
            pass
        await context.message.delete()

    @commands.command(name='unload')
    @commands.has_role(maintenance['maintananceRole'])
    async def unload_cog(self, context, extension):
        """trennt ein laufendes Modul um es ohne Impact berabeiten oder entfernen zu können."""
        extension_path = 'cogs.' + extension
        member = context.message.author
        smbed = discord.Embed(title='Unload erfolgreich', description=f'Das Modul "{extension}" ist nun nicht mehr benutzbar.', color=discord.Color.green())
        NFmbed = discord.Embed(title='Unload fehlgeschlagen', description=f'Das Modul "{extension}" existiert nicht oder ist falsch geschrieben.', color=discord.Color.red())
        NLmbed = discord.Embed(title='Unload fehlgeschlagen', description=f'Das Modul "{extension}" konnte nicht unloaded werden da es nie geladen war', color=discord.Color.red())
        wmbed = discord.Embed(title='Dein Ernst?', description='Was glaubst du was passiert wenn du das hier entfernst? Denk doch mal nach!', color=discord.Color.orange())

        if extension == 'bot-managing':
            await context.send(embed=wmbed)
            logger.critical(str(member) + ' tried to unload the cog ' + extension + ' that shouldnt be unloaded')
        else:
            try:
                self.bot.unload_extension(extension_path)
                await context.send(embed=smbed)
                logger.info('cog ' + extension + ' unloaded by ' + str(member))
            except ExtensionNotFound:
                await context.send(embed=NFmbed)
                logger.warning(str(member) + ' tried to unload the cog ' + extension + ' but it doesnt exist')
                pass
            except ExtensionNotLoaded:
                await context.send(embed=NLmbed)
                logger.warning(str(member) + ' tried to unload the cog ' + extension + ' but it was not loaded in the first place')
                pass

            await context.message.delete()

    @commands.command(name='reload')
    @commands.has_role(maintenance['maintananceRole'])
    async def reload_cog(self, context, extension):
        """lädt ein Modul neu wenn es sich geändert haben sollte."""
        extension_path = 'cogs.' + extension
        member = context.message.author
        smbed = discord.Embed(title='Reload erfolgreich', description=f'Das Modul "{extension}" ist nun wieder benutzbar.', color=discord.Color.green())
        NLmbed = discord.Embed(title='Reload fehlgeschlagen', description=f'Das Modul "{extension}" konnte nicht reloaded werden da es nie geladen war', color=discord.Color.red())
        NFmbed = discord.Embed(title='Reload fehlgeschlagen', description=f'Das Modul "{extension}" existiert nicht oder ist falsch geschrieben', color=discord.Color.red())
        NEmbed = discord.Embed(title='Reload fehlgeschlagen', description=f'Das Modu "{extension}" hat keine Setup Funtion', color=discord.Color.red())
        Fmbed = discord.Embed(title='Load fehlgeschlagen', description=f'Das Modul "{extension}" hatte ein Problem beim ausführen der Setup Funktion', color=discord.Color.red())

        try:
            self.bot.reload_extension(extension_path)
            await context.send(embed=smbed)
            logger.info('cog ' + extension + ' reloaded by ' + str(member))
        except ExtensionNotLoaded:
            await context.send(embed=NLmbed)
            logger.warning(str(member) + ' tried to reload the cog ' + extension + ' but it was not loaded in the first place')
        except ExtensionNotFound:
            await context.send(embed=NFmbed)
            logger.warning(str(member) + ' tried to reload the cog ' + extension + ' but it doesnt exist')
        except NoEntryPointError:
            await context.send(embed=NEmbed)
            logger.warning(str(member) + ' tried to reload the cog ' + extension + ' but it has no setup funtion')
        except ExtensionFailed:
            await context.send(embed=Fmbed)
            logger.warning(str(member) + ' tried to reload the cog ' + extension + ' but the setup function had an execution error')

        await context.message.delete()
        
def setup(bot):
    bot.add_cog(BotManaging(bot))