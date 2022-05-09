import logging
import os
import discord
from skynet_bot import maintenance
from discord.ext import commands

source = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger('SkyNet-Core.BotCommands')


class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='list_loaded')
    @commands.has_role(maintenance['maintananceRole'])
    async def list_loaded_cogs(self, ctx):
        """list all cogs loaded on the server"""

    @commands.command(name='list_available')
    @commands.has_role(maintenance['maintananceRole'])
    async def list_available_cogs(self, ctx):
        """Listet alle verfügbaren Module auf"""

        ListModulesField = ''
        
        try:
            for CogFile in os.listdir(source):
                if CogFile.endswith('.py'):
                    ListModulesField += '* ' + str(CogFile[:-3]) + '\n'
        
        except:
            logger.warning('could not list cogs')

        embed = discord.Embed(
            title='List of Modules',
            description=ListModulesField,
            color=discord.Color.blue()
        )

        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(name='load')
    @commands.has_role(maintenance['maintananceRole'])
    async def load_cog(self, ctx, extension):
        """Lädt ein Modul um ein neustart des Bots zu vermeiden."""

        extension_path = 'cogs.' + extension
        member = ctx.message.author

        try:
            self.bot.load_extension(extension_path)

            embed = discord.Embed(
                title='Load erfolgreich',
                description=f'Das Modul {extension} ist nun benutzbar.',
                color=discord.Color.green()
            )

            logger.info(f'cog {extension} loaded by {member}')

        except Exception as e:
            embed = discord.Embed(
                title='Load fehlgeschlagen',
                description=f'Das Modul {extension} konnte nicht geladen werden.',
                color=discord.Color.red()
            )

            embed.add_field(
                name='Error',
                value=e
            )

            logger.warning(
                f'{member} tried to load the cog {extension} but the following Error occured:\n {e}')

        finally:
            await ctx.send(embed=embed)
            await ctx.message.delete()

    @commands.command(name='unload')
    @commands.has_role(maintenance['maintananceRole'])
    async def unload_cog(self, ctx, extension):
        """Trennt ein Modul um es ohne Impact berabeiten oder entfernen zu können."""

        extension_path = 'cogs.' + extension
        member = ctx.message.author

        if extension == 'bot':
            embed = discord.Embed(
                title='Dein Ernst?',
                description='Was glaubst du was passiert wenn du das hier entfernst? Denk doch mal nach!',
                color=discord.Color.orange()
            )

            await ctx.send(embed=embed)

            logger.critical(
                f'{member} tried to unload the cog {extension} that shouldnt be unloaded')

        else:
            try:
                self.bot.unload_extension(extension_path)

                embed = discord.Embed(
                    title='Unload erfolgreich',
                    description=f'Das Modul {extension} ist nun nicht mehr benutzbar.',
                    color=discord.Color.green()
                )

                logger.info(f'cog {extension} unloaded by {member}')

            except Exception as e:
                embed = discord.Embed(
                    title='Unload fehlgeschlagen',
                    description=f'Das Modul {extension} konnte nicht getrennt werden.',
                    color=discord.Color.red()
                )

                embed.add_field(
                    name='Error',
                    value=e
                )

                logger.warning(
                    f'{member} tried to unload the cog {extension} but the following Error occured:\n{e}')

            finally:
                await ctx.send(embed=embed)
                await ctx.message.delete()

    @commands.command(name='reload')
    @commands.has_role(maintenance['maintananceRole'])
    async def reload_cog(self, ctx, extension):
        """Lädt ein Modul neu wenn es sich geändert haben sollte."""

        extension_path = 'cogs.' + extension
        member = ctx.message.author

        try:
            self.bot.reload_extension(extension_path)

            embed = discord.Embed(
                title='Reload erfolgreich',
                description=f'Das Modul {extension} ist nun wieder benutzbar.',
                color=discord.Color.green()
            )

            logger.info(f'cog {extension} reloaded by {member}')

        except Exception as e:
            embed = discord.Embed(
                title='Reload fehlgeschlagen',
                description=f'Das Modul {extension} konnte nicht neugeladen werden.',
                color=discord.Color.red()
            )

            embed.add_field(
                name='Error',
                value=e
            )

            logger.warning(
                f'{member} tried to reload the cog {extension} but the following Error occured:\n{e}')

        finally:
            await ctx.send(embed=embed)
            await ctx.message.delete()


def setup(bot):
    bot.add_cog(BotCommands(bot))
