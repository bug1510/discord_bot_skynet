import os, logging
from logging.handlers import TimedRotatingFileHandler
from discord.ext import commands
from utils.file_handler import FileHandlingUtils as fhu
from skynet_bot.skynet_bot import logpath
from skynet_bot.skynet_bot import cogpath


class InitBotFunctions(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def init_logger(self) -> None:
        self.bot.logpath = logpath
        if not os.path.exists(self.bot.logpath): #checks if log folder exist if not creates one
            os.makedirs(self.bot.logpath)
        self.bot.logger = logging.getLogger('SkyNet')
        self.bot.logger.setLevel(logging.INFO)

        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        rotatinglogs = TimedRotatingFileHandler(
            filename=self.bot.logpath + '/skynet_bot.log',
            when="midnight",
            interval=1,
            backupCount=5
            )
        rotatinglogs.setLevel(logging.INFO)
        rotatinglogs.setFormatter(format)

        self.bot.logger.addHandler(rotatinglogs)
        self.bot.logger.info('LoggingHandler | finished initiating the logging')
        self.bot.logger.info(f'LoggingHandler | the logpath was set to: {self.bot.logpath}')

    async def init_cogs(self) -> None:
        self.bot.cogpath = cogpath
        self.bot.logger.info(f' CogHandler | The Cogpath was set to: {self.bot.cogpath}')
        extensions = fhu.cog_listing(path=self.bot.cogpath, extensions=[])
        for extension in extensions:
            try:
                if extension not in self.bot.loaded_cogs:
                    await self.bot.load_extension(extension)
                    self.bot.loaded_cogs.append(extension)
                    self.bot.logger.info(f'CogHandler | The following Module was loaded into the bot: {extension}')
            except Exception as e:
                self.bot.logger.critical(f'CogHandler | failed to initiate the modul {extension}, due to: {e}')
        self.bot.logger.info('CogHandler | finished initiating the modules')

    async def init_database_handler(self) -> None:
        multi_server_sync = self.bot.community_settings['MultiServerSync']
        leveling = self.bot.community_settings['Leveling']

        try:
            if multi_server_sync['Enalbled']:
                await self.bot.load_extension('utils.ms_db_handler')
                self.bot.loaded_cogs.append('utils.ms_db_handler')
                self.bot.logger.info(f'InitFunctions | initiating the Multi Server Database Handler')

            elif leveling['Enalbled'] and not multi_server_sync['Enalbled']:
                await self.bot.load_extension('utils.ss_db_handler')
                self.bot.loaded_cogs.append('utils.ss_db_handler')
                self.bot.logger.info(f'InitFunctions | initiating the Single Server Database Handler')

        except Exception as e:
            self.bot.logger.critical(f'InitFunctions | initiating the database handler failed due to: {e}')

async def setup(bot):
    await bot.add_cog(InitBotFunctions(bot))