import discord, os, json, logging
from discord.ext import commands
import utils.leveling.leveling_utils as leveling_utils
import utils.server.server_utils as su
from discord.utils import get

logger = logging.getLogger('SkyNet-Core.MemberCommands')

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../data/config/config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

class MemberCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rank')
    async def rank(self, ctx):
        '''Gibt dir eine genaue Übersicht über dein Level und deine Erfahrungspunkte.'''
        guild_id = ctx.message.author.guild.id
        user_nick = ctx.message.author.display_name
        embed =discord.Embed(title=f'{user_nick}´s Rank Card', color=discord.Color.blurple())

        if os.path.exists(f'{source}/../data/{str(guild_id)}.db'):
            user_data = await leveling_utils.get_rank(ctx)

            user_level = user_data[4]
            user_exp = user_data[5]

            embed.add_field(name='Level', value=user_level, inline=True)
            embed.add_field(name='Erfahrungspunkte', value=user_exp, inline=True)

            await ctx.send(embed=embed)
        else:
            return

    @commands.command(name='tcc')
    async def create_temp_channel(self, ctx, userlimit=0):
        '''Erstellt dir und deinen Freunden einen Temporären Raum.'''
        guild = ctx.message.guild
        member = ctx.message.author
        place = get(guild.categories, name=maintenance['tmpCatName'])

        embed = discord.Embed(title='empty', color=discord.Color.dark_grey())

        if not place:
            place = await su.create_category(guild=guild, name=maintenance['tmpCatName'], member='SkyNet Bot', embed=embed)
        vc, embed = await su.create_voicechannel(guild=guild, name=maintenance['tempChannelName'], userlimit=userlimit, place=place, embed=embed)

        try:
            await member.move_to(vc)
        except:
            return
        
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(MemberCommands(bot))