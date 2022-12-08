import discord, os
from discord.ext import commands
from discord.utils import get
from utils.custom_object import CustomObject as co

class MemberCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rank')
    async def rank(self, ctx):
        '''Gibt dir eine genaue Übersicht über dein Level und deine Erfahrungspunkte.'''
        member = ctx.message.author
        user_nick = ctx.message.author.display_name

        db_handler = self.bot.get_cog(str(self.bot.db_handler))
        embed = discord.Embed(title=f'{user_nick}´s Rank Card', color=discord.Color.blurple())

        try:
            user_data = await db_handler.get_user_exp_and_level(ctx.message.guild.id, member.id, str(member))

            user_level = user_data[4]
            user_exp = user_data[5]

            embed.add_field(name='Level', value=user_level, inline=True)
            embed.add_field(name='Erfahrungspunkte', value=user_exp, inline=True)
        except Exception as e:
            embed.add_field(name='!ERROR!', value='Please check your Logs' )
            self.bot.logger.warning(f'MemberCommands | Getting the Rank Card for User {member} failed due to: {e}')
        finally:
            await ctx.send(embed=embed)

    @commands.command(name='tcc')
    async def create_temp_channel(self, ctx, userlimit=0):
        '''Erstellt dir und deinen Freunden einen Temporären Raum.'''
        embed = discord.Embed(title='empty', color=discord.Color.dark_grey())
        member = ctx.message.author

        custom_channel = co(guild=ctx.message.guild, name=self.bot.config['tmpCatName'], embed=embed)
        custom_channel.place = get(ctx.guild.categories, name=self.bot.config['tmpCatName'])
        custom_channel.channel = [str(self.bot.config['tempChannelName'])]
        custom_channel.userlimit = userlimit

        channel_manager = self.bot.get_cog('ChannelHandlingUtils')

        if not custom_channel.place:
            custom_channel = await channel_manager.create_category(custom_channel)
        self.bot.logger.info(f'MemberCommands | created the TempChannel Category')

        custom_channel = await channel_manager.create_voicechannel(custom_channel)
        self.bot.logger.info(f'MemberCommands | created a TemmpChannel for {member}')
        try:
            await member.move_to(custom_channel.vc)
        except:
            return
        
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(MemberCommands(bot))