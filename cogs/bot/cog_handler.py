import discord
from discord.ext import commands
from utils.file_handler import FileHandlingUtils as fhu
from skynet_bot import cogpath

class CogHandler(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def init_cogs(self) -> None:
        self.bot.cogpath = cogpath
        self.bot.logger.info(f' CogHandler | The Cogpath was set to: {self.bot.cogpath}')
        extensions = fhu.cog_finder(path=self.bot.cogpath, extensions=[])
        for extension in extensions:
            try:
                if extension not in self.bot.loaded_cogs:
                    await self.bot.load_extension(extension)
                    self.bot.loaded_cogs.append(extension)
                    self.bot.logger.info(f'CogHandler | The following Module was loaded into the bot: {extension}')
            except Exception as e:
                self.bot.logger.critical(f'CogHandler | failed to initiate the modul {extension}, due to: {e}')
        self.bot.logger.info('CogHandler | finished initiating the modules')

    async def list_available_cogs(self, embed):
            ListModulesField = []
            ListOfModules = ''
            try:
                for CogFile in (fhu.cog_finder(path=self.bot.cogpath, extensions=ListModulesField)):
                    CogFileSplitted = CogFile.split('.')
                    CogFileSplitted.reverse()
                    ListOfModules += (f'-{CogFileSplitted[0]}\n')
                embed.add_field(name='Found:', value=ListOfModules, inline=False)
            except Exception as e:
                self.bot.logger.critical(f'CogHandler | could not list cogs because of: {e}')
                embed.add_field(
                    name='!Error!',
                    value='There was an error listing the cogs. Check Logs!',
                    inline=False
                )
                embed.color=discord.Color.red()
            finally:
                return embed

    async def load_cogs(self, member: str, embed, extensions:list):
        for extension in extensions:
            try:
                if extension not in self.bot.loaded_cogs:
                    await self.bot.load_extension(extension)
                    self.bot.logger.warning(f'CogHandler | cog {extension} loaded by {member}')
                    embed.add_field(name='!Success!', value='Modul was loaded')
                    embed.color=discord.Color.green()
            except Exception as e:
                embed.add_field(name='!Error!', value=e)
                self.bot.logger.critical(f'CogHandler | {member} tried to load the cog {extension} but the following Error occured:\n {e}')
                embed.color=discord.Color.red()
            finally:
                return embed

    async def unload_cogs(self, member: str, embed, extensions:list):
        for extension in extensions:
            match str(extension):
                case extension.startswith('cogs.commands.'):
                    try:
                        self.bot.unload_extension(extension)
                        self.bot.logger.warning(f'CogHandler | cog {extension} unloaded by {member}')
                        embed.add_field(name='!Success!', value='Modul was unloaded')
                        embed.color=discord.Color.green()
                    except Exception as e:
                        embed.add_field(name='Error', value=e)
                        embed.color=discord.Color.red()
                        self.bot.logger.critical(f'CogHandler | {member} tried to unload the cog {extension} but the following Error occured:\n{e}')
                    finally:
                        return embed
                case _:
                    embed = discord.Embed(
                        title='Dein Ernst?',
                        description='Was glaubst du was passiert wenn du das hier entfernst? Denk doch mal nach!',
                        color=discord.Color.orange()
                    )
                    self.bot.logger.critical(f'CogHandler | {member} tried to unload the cog {extension} that shouldnt be unloaded')
                    return embed

    async def reload_cogs(self, member: str, embed, extensions: list):
        for extension in extensions:
            try:
                self.bot.reload_extension(extension)
                self.logger.info(f'CogHandler | cog {extension} reloaded by {member}')
                embed.add_field(name='!Success!', value='Modul was reloaded')
                embed.color=discord.Color.green()
            except Exception as e:
                embed.add_field(name='Error',value=e)
                embed.color=discord.Color.red()
                self.logger.critical(f'CogHandler | {member} tried to reload the cog {extension} but the following Error occured:\n{e}')
            finally:
                return embed

async def setup(bot):
    await bot.add_cog(CogHandler(bot))