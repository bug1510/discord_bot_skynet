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

        user = member.display_name
        embed = discord.Embed(
            title = 'GameChannelCreate',
            description = f'Das Erstellen wurde von {user} ausgelöst.',
            color = discord.Color.dark_gold()
            )

        place, embed = await su.create_category(guild=guild, name=space_name, member=member, embed=embed)

        role, embed = await su.create_role(guild=guild, name=space_name, member=member, embed=embed)

        embed = await su.set_standard_permission_for_cat(guild=guild, place=place, role=role, embed=embed)

        embed = await su.create_textchannel(guild=guild, name=space_name, place=place, embed=embed)

        embed = await su.create_voicechannel(guild=guild, name=space_name, place=place, embed=embed)

        await ctx.send(embed=embed)
        await ctx.message.delete()
        
    @commands.command('gcd')
    @commands.has_role(maintenance['maintananceRole'])

    async def game_channel_delete(self, context, gamename):

        """Dieser Befehl ist administrativ und entfernt eine Rolle ihre Kategorie und alle Channel darin"""
        guild = context.message.guild
        member = context.message.author
        gamerole = get(guild.roles, name=gamename)
        place = get(guild.categories, name= '<##>' + str(gamename))
        user = member.display_name
        embed = discord.Embed(
            title = 'GameChannelDelete',
            description = f'Das Löschen wurde von {user} ausgelöst.',
            color = discord.Color.dark_gold()
            )
        
        try:
            for tc in place.text_channels:
                await tc.delete(reason=None)
            
            logger.info(str(member) + ' deleted all Text Channels from the Category ' + str(gamename) + ' successfully')
            embed = embed.add_field(
                name= '!Success deleting Text Channels!',
                value= 'Die Text Channels aus ' + str(place) + ' wurden gelöscht',
                inline=False
            )
        except:
            logger.warning(str(member) + ' tried to delete all Text Channels from the Category' + str(gamename) + ' but it failed')
            embed = embed.add_field(
                name= '!Failure deleting Text Channels',
                value= 'Beim löschen der Text Channels für ' + str(place) + ' ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
                inline=False
            )
        
        try:
            for vc in place.voice_channels:
                await vc.delete(reason=None)
            
            logger.info(str(member) + ' deleted all Voice Channels from the Category ' + str(gamename) + ' successfully')
            embed = embed.add_field(
                name= '!Success deleting Voice Channels!',
                value= 'Die Voice Channels für ' + str(place) + ' wurden gelöscht.',
                inline=False
            )
        except:
            logger.warning(str(member) + ' tried to delete all Voice Channels from the Category ' + str(gamename) + ' but it failed')
            embed = embed.add_field(
                name= '!Failure deleting Voice Channels',
                value= 'Beim löschen der Voice Channels für ' + str(place) + ' ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
                inline=False
            )

        try:
            await place.delete(reason=None)

            logger.info(str(member) + ' deleted the Category ' + str(gamename) + ' successfully')
            embed = embed.add_field(
                name= '!Success deleting Category!',
                value= 'Die Kategorie ' + str(place) + ' wurde gelöscht.',
                inline=False
            )
        except:
            logger.warning(str(member) + ' tried to delete the Category ' + str(gamename) + ' but it failed')
            embed = embed.add_field(
                name= '!Failure deleting Category!',
                value= 'Beim löschen der Categrory ' + str(place) + ' ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
                inline=False
            )

        try:
            await gamerole.delete(reason=None)

            logger.info(str(member) + ' deleted the role to the Category ' + str(gamename) + ' successfully')
            embed = embed.add_field(
                name= '!Success deleting Category connected Role!',
                value= 'Die zu ' + str(place) + ' gehörige Rolle wurde gelöscht.',
                inline=False
            )
        except:
            logger.warning(str(member) + ' tried to delete the role to the Category ' + str(gamename) + ' but it failed')
            embed = embed.add_field(
                name= '!Failure deleting Category connected Role!',
                value= 'Beim löschen der zu ' + str(place) + ' gehörigen Rolle ist etwas schief gelaufen.',
                inline=False
            )

        await context.send(embed=embed)
        await context.message.delete()

    @commands.command()
    @commands.has_role(maintenance['maintananceRole'])
    async def clear(self, context, number=50):
        channel = context.message.channel
        member = context.message.author
        user = context.message.author.display_name
        embed = discord.Embed(
            title='!ACHTUNG!',
            description=f'{number} alte Nachrichten wurden aus diesem Chat gelöscht,\nvon deinem Admin: {user}',
            color=discord.Color.dark_red())
            
        await context.message.delete()
        logger.info(f'{number} alte Nachrichten wurden aus diesem Chat gelöscht, vom Admin: {member}')
        await channel.purge(limit=int(number), oldest_first=True, bulk=False)
        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(AdminCommands(bot))