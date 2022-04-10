import discord, os, json, logging
from discord.ext import commands
from discord.utils import get

import maintenance.server_utils as su

logger = logging.getLogger(__name__)

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='gcc')
    @commands.has_role(maintenance['maintananceRole'])

    async def game_channel_create(self, ctx, space_name):

        """Dieser Befehl ist administrativ und legt eine ganze Rolle ihre Kategorie und eigene Channel an"""

        guild = ctx.message.guild
        member = ctx.message.author
        logger.info(str(member) + ' tried to create category ' + str(space_name))

        user_icon = ctx.message.author.avatar_url_as(static_format='png', size=128)

        user = member.display_name
        embed = discord.Embed(
            title = 'GameChannelCreate',
            description = f'Das Erstellen wurde von {user} ausgelöst.',
            color = discord.Color.dark_gold()
            )

        embed.set_thumbnail(url=user_icon)

        place, embed = await su.create_category(guild=guild, name=space_name, member=member, embed=embed)

        role, embed = await su.create_role(guild=guild, name=space_name, member=member, embed=embed)

        embed = await su.set_standard_permission_for_cat(guild=guild, place=place, role=role, embed=embed)

        embed = await su.create_textchannel(guild=guild, name=maintenance['standardTextChannels'], place=place, embed=embed)

        embed = await su.create_voicechannel(guild=guild, name=maintenance['standardVoiceChannels'],userlimit=maintenance['userLimit'], place=place, embed=embed)

        await ctx.send(embed=embed)
        await ctx.message.delete()
        
    @commands.command('gcd')
    @commands.has_role(maintenance['maintananceRole'])

    async def game_channel_delete(self, ctx, space_name):

        """Dieser Befehl ist administrativ und entfernt eine Rolle ihre Kategorie und alle Channel darin"""
        
        guild = ctx.message.guild
        member = ctx.message.author
        role = get(guild.roles, name=space_name)
        place = get(guild.categories, name=str(space_name))
        user = member.display_name
        
        user_icon = ctx.message.author.avatar_url_as(static_format='png', size=128)

        embed = discord.Embed(
            title = 'GameChannelDelete',
            description = f'Das Löschen wurde von {user} ausgelöst.',
            color = discord.Color.dark_gold()
            )

        embed.set_thumbnail(url=user_icon)

        embed = await su.delete_voicechannel(place=place, name='all', member=member, embed=embed)

        embed = await su.delete_textchannel(place=place, name='all', member=member, embed=embed)

        embed = await su.delete_category(place=place, member=member, embed=embed)

        embed = await su.delete_role(role=role, member=member, embed=embed)

        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    @commands.has_role(maintenance['maintananceRole'])
    async def clear(self, ctx, number=50):
        channel = ctx.message.channel
        member = ctx.message.author
        user = ctx.message.author.display_name
        
        user_icon = ctx.message.author.avatar_url_as(static_format='png', size=128)

        embed = discord.Embed(
            title='!ACHTUNG!',
            description=f'{number} alte Nachrichten wurden aus diesem Chat gelöscht,\nvon deinem Admin: {user}',
            color=discord.Color.dark_red())
        
        embed.set_thumbnail(url=user_icon)

        await ctx.message.delete()
        logger.info(f'{number} alte Nachrichten wurden aus diesem Chat gelöscht, vom Admin: {member}')
        await channel.purge(limit=int(number), oldest_first=True, bulk=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(AdminCommands(bot))