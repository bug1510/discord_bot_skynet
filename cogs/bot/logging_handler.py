import os, logging
from logging.handlers import TimedRotatingFileHandler
from discord.ext import commands

class LoggingHandler(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def init_logger(self):
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

async def setup(bot):
    await bot.add_cog(LoggingHandler(bot))