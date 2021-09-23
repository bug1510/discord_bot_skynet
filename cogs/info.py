import discord,os
from discord import colour
from discord.ext import commands
import logging,platform,psutil
from meeseeks_bot import maintenance

logger = logging.getLogger(__name__)
source = os.path.dirname(os.path.abspath(__file__))

class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='serverinfo')
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

    @commands.command(name='communityinfo')
    async def get_communityinfo(self, ctx):
        """ Show all Infos about the Community """

        guild_icon = ctx.message.guild.icon_url_as(static_format='png', size=128)
        guild_name = ctx.message.guild.name
        guild_owner = ctx.message.guild.owner
        guild_roles = ctx.message.guild.roles
        guild_members = ctx.message.guild.member_count
        twitch_url = maintenance['twitchLink']

        number_of_roles = 0

        for r in guild_roles:
            number_of_roles += 1

        embed = discord.Embed(title=f'Info about {guild_name}',color=colour.Color.blurple())
        embed.set_thumbnail(url=guild_icon)
        embed.add_field(name='Owner', value=guild_owner, inline=True)
        embed.add_field(name='Number of Roles', value=number_of_roles, inline=True)
        embed.add_field(name='Number of Members(including Bots)', value=guild_members, inline=True)
        embed.add_field(name=f'Twitch Link of {guild_owner}', value=twitch_url, inline=True)

        await ctx.send(embed=embed)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(InfoCommands(bot))