import discord, os, logging
from discord.ext import commands
from discord.utils import get
from utils.bot.config_handler import ConfigHandlingUtils as cohu
import utils.member.leveling.leveling_utils as lvlu
import utils.server.channel_handling_utils as su

class MemberCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('SkyNet-Core.MemberCommands')
        self.source = None
        self.config = cohu.json_handler(filename=str('config'))

    @commands.command(name='rank')
    async def rank(self, ctx):
        '''Gibt dir eine genaue Übersicht über dein Level und deine Erfahrungspunkte.'''
        guild_id = ctx.message.author.guild.id
        user_nick = ctx.message.author.display_name
        embed =discord.Embed(title=f'{user_nick}´s Rank Card', color=discord.Color.blurple())

        if os.path.exists(f'{self.source}/../data/{str(guild_id)}.db'):
            user_data = await lvlu.get_rank(ctx)

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
        place = get(guild.categories, name=self.config['tmpCatName'])

        embed = discord.Embed(title='empty', color=discord.Color.dark_grey())

        if not place:
            place = await su.create_category(guild=guild, name=self.config['tmpCatName'], member='SkyNet Bot', embed=embed)
        vc, embed = await su.create_voicechannel(guild=guild, name=self.config['tempChannelName'], userlimit=userlimit, place=place, embed=embed)

        try:
            await member.move_to(vc)
        except:
            return
        
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(MemberCommands(bot))