import discord
from discord.ext import commands
from discord.utils import get
from cogs.utils.custom_object import CustomObject as co

class MemberCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='poll')
    async def create_poll(self, ctx, q1, ans1, ans2, ans3='0', ans4='0', ans5='0', ans6='0', ans7='0', ans8='0', ans9='0', ans10='0'):
        '''Mit dem Befehl poll erstellt Mr.Meeseeks dir eine Abstimmung um dir Klarheit zu verschaffen.'''

        user_icon = ctx.message.author.avatar_url_as(static_format='png', size=128)
        member = ctx.message.author.display_name
        answeres = ''

        answeres += '1️⃣' + str(ans1) + '\n'
        answeres += '2️⃣' + str(ans2) + '\n'

        if not ans3 == '0':
            answeres += '3️⃣' + str(ans3) + '\n'
        if not ans4 == '0':
            answeres += '4️⃣' + str(ans4) + '\n'
        if not ans5 == '0':
            answeres += '5️⃣' + str(ans5) + '\n'
        if not ans5 == '0':
            answeres += '6️⃣' + str(ans6) + '\n'
        if not ans5 == '0':
            answeres += '7️⃣' + str(ans7) + '\n'
        if not ans5 == '0':
            answeres += '8️⃣' + str(ans8) + '\n'
        if not ans5 == '0':
            answeres += '9️⃣' + str(ans9) + '\n'
        if not ans5 == '0':
            answeres += '🔟' + str(ans10) + '\n'

        embed = discord.Embed(title=f'{member} fragt euch: ' + q1, description=answeres, color=discord.Color.dark_purple())
        embed.set_thumbnail(url=user_icon)

        embed.add_field(name='Info', value='Alle Reaktionswerte -1 sehen!', inline=False )

        msg = await ctx.send(embed=embed)

        await msg.add_reaction(emoji='1️⃣')
        await msg.add_reaction(emoji='2️⃣')

        if not ans3 == '0':
            await msg.add_reaction(emoji='3️⃣')
        if not ans4 == '0':
            await msg.add_reaction(emoji='4️⃣')
        if not ans5 == '0':
            await msg.add_reaction(emoji='5️⃣')
        if not ans6 == '0':
            await msg.add_reaction(emoji='6️⃣')
        if not ans7 == '0':
            await msg.add_reaction(emoji='7️⃣')
        if not ans8 == '0':
            await msg.add_reaction(emoji='8️⃣')
        if not ans9 == '0':
            await msg.add_reaction(emoji='9️⃣')
        if not ans10 == '0':
            await msg.add_reaction(emoji='🔟')

        await ctx.message.delete()

    @commands.command(name='rank')
    async def rank(self, ctx):
        '''Gibt dir eine genaue Übersicht über dein Level und deine Erfahrungspunkte.'''
        member = ctx.message.author
        user_nick = ctx.message.author.display_name

        db_handler = self.bot.get_cog('DBHandler')
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

        custom_channel = co(guild=ctx.message.guild, name=self.bot.server_settings['TempCatName'], embed=embed)
        custom_channel.place = get(ctx.guild.categories, name=self.bot.server_settings['TempCatName'])
        custom_channel.channel = [str(self.bot.server_settings['TempChannelName'])]
        custom_channel.userlimit = userlimit

        channel_manager = self.bot.get_cog('ChannelManager')

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

    @commands.command(name='communityinfo')
    async def get_communityinfo(self, ctx):
        """ Show all Infos about the Community """

        guild_icon = ctx.message.guild.icon_url_as(static_format='png', size=128)
        guild_name = ctx.message.guild.name
        guild_owner = ctx.message.guild.owner
        guild_roles = ctx.message.guild.roles
        guild_members = ctx.message.guild.member_count

        number_of_roles = 0

        for r in guild_roles:
            number_of_roles += 1

        embed = discord.Embed(title=f'Info about {guild_name}',color=discord.colour.Color.blurple())
        embed.set_thumbnail(url=guild_icon)
        embed.add_field(name='Owner', value=guild_owner, inline=True)
        embed.add_field(name='Number of Roles', value=number_of_roles, inline=True)
        embed.add_field(name='Number of Members(including Bots)', value=guild_members, inline=True)
        #embed.add_field(name=f'Twitch Link of {guild_owner}', value=twitch_url, inline=True)

        await ctx.send(embed=embed)
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(MemberCommands(bot))