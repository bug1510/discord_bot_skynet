import discord,os
from discord import client
from discord.ext import commands
from discord.utils import get
import logging,platform,psutil
logger = logging.getLogger(__name__)
source = os.path.dirname(os.path.abspath(__file__))

class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='serverinfo')
    @commands.has_role('El-Special')

    async def get_serverinfo(self, context):
        """ Show Server Informations """
        embed = discord.Embed(title='Serverinformations',
                              description='Informations about the Backend Server',
                              color=discord.Color.orange())

        SystemInfoField = 'Platform : ' + platform.system() + '\n'
        SystemInfoField += 'Version  : ' + platform.version() + '\n'
        SystemInfoField += 'CPU      : ' + platform.processor()

        embed.add_field(name='System Informations',
                        value=SystemInfoField,
                        inline=False) 
        
        RamInfoField = 'Total    : ' + str(round(((psutil.virtual_memory()[0] / 1024 ) / 1024) / 1024,0)) + ' GB \n'
        RamInfoField += 'Free     : ' + str(round(((psutil.virtual_memory()[4] / 1024 ) / 1024) / 1024,0)) + ' GB'

        embed.add_field(name='Memory Informations',
                        value=RamInfoField,
                        inline=False) 

        file = discord.File(source + "/../img/confidential.png", filename="confidential.png")
        embed.set_thumbnail(url="attachment://confidential.png")

        await context.send(file=file,embed=embed)
        
        await context.message.delete()

def setup(bot):
    bot.add_cog(InfoCommands(bot))


