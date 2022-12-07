import discord, os, logging
from discord.ext import commands
from discord.utils import get

logger = logging.getLogger('SkyNet-Core.JFWCommands')

source = os.path.dirname(os.path.abspath(__file__))

class JFWCommands(commands.Cog):
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

    @commands.command(name='Kettenbrief')
    async def invite_group(self, ctx, group, invite_message):

        user_icon = ctx.message.author.avatar_url_as(static_format='png', size=128)
        member = ctx.message.author.display_name

        guild = ctx.message.guild
        role = get(guild.roles, name=group)

        members = role.members

        embed = discord.Embed(title=f'{member} möchte dir folgendes mitteilen:', description=invite_message, color=discord.Color.purple())
        embed.set_thumbnail(url=user_icon)

        embeds = discord.Embed(title='!Alle Nutzer haben die Nachricht erhalten!', color=discord.Color.green())

        faileduser = ''

        embedf = discord.Embed(title=f'!Folgende Nutzer haben die Nachricht leider nicht erhalten!', color=discord.Color.red())

        failed = False

        for m in members:
            try:
                c = await m.create_dm()
                await c.send(embed=embed)
            except:
                if 'Mr Meeseeks' in str(m):
                    return
                else:
                    failed = True
                    faileduser += str(m) + '\n'
        
        if failed:
            embedf.add_field(
                name='Die Nutzer waren..',
                value=faileduser,
                inline=False
            )
            
            await ctx.send(embed=embedf)

        else:
            await ctx.send(embed=embeds)

    @commands.command(name='cchannel')
    @commands.has_any_role(
        'AK-digitale-Infrastruktur',
        'AK-Social-Media',
        'AK-Strukturaufbau/Mitgliederwerbung',
        'AK-Agenda-&-Inhalte',
        'AK-Presse-&-Öffentlichkeit'
    )
    async def create_channel(self, ctx, channel_name, channel_type, userlimit=None):
        
        roles = ['AK-digitale-Infrastruktur',
        'AK-Social-Media',
        'AK-Strukturaufbau/Mitgliederwerbung',
        'AK-Agenda-&-Inhalte',
        'AK-Presse-&-Öffentlichkeit'
        ]

        guild_id = ctx.message.guild
        member = ctx.message.author

        channel = []
        channel.append(channel_name)

        for mr in member.roles:
            if str(mr) in roles:
                category_name = get(guild_id.categories, name=str(mr))

        embed = discord.Embed(
            title='Create Channel',
            description='Das Erstellen wurde von ausgelöst.',
            color=discord.Color.dark_gold()
        )
        try:
            if str(channel_type) == 'text':
                await su.create_textchannel(
                    guild=guild_id,
                    name=channel,
                    place=category_name,
                    embed=embed
                    )
            elif str(channel_type) == 'voice':
                if userlimit == None:
                    userlimit = 0
                await su.create_voicechannel(
                    guild=guild_id,
                    name=channel,
                    userlimit=userlimit,
                    place=category_name,
                    embed=embed
                )
        except Exception as e:
            logger.warning(f'Category wasnt created due to an error: {e}')
            embed.add_field(
                name= '!Failure creating Category!',
                value= f'Die Kategorie konnte nicht erstellt werden. \n{e}',
                inline=False
            )
        finally:
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(JFWCommands(bot))