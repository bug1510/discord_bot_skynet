import logging, os, discord
from discord.ext import commands
from utils.bot.config_handler import ConfigHandlingUtils as cohu

needed_role = cohu().json_handler(filename=str('config.json'))
class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('SkyNet-Core.BotCommands')
        self.source = os.path.dirname(os.path.abspath(__file__))
    
    @commands.command(name='list_loaded')
    @commands.has_role(needed_role['maintananceRole'])
    async def list_loaded_cogs(self, ctx):
        """list all cogs loaded on the server"""

    @commands.command(name='list_available')
    @commands.has_role(needed_role['maintananceRole'])
    async def list_available_cogs(self, ctx):
        """Listet alle verfügbaren Module auf"""



    @commands.command(name='load')
    @commands.has_role(needed_role['maintananceRole'])
    async def load_cog(self, ctx, extension):
        """Lädt ein Modul um ein neustart des Bots zu vermeiden."""



    @commands.command(name='unload')
    @commands.has_role(needed_role['maintananceRole'])
    async def unload_cog(self, ctx, extension):
        """Trennt ein Modul um es ohne Impact berabeiten oder entfernen zu können."""

 

    @commands.command(name='reload')
    @commands.has_role(needed_role['maintananceRole'])
    async def reload_cog(self, ctx, extension):
        """Lädt ein Modul neu wenn es sich geändert haben sollte."""



async def setup(bot):
    await bot.add_cog(BotCommands(bot))
