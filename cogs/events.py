import json, os, logging, discord
from discord.ext import commands
from discord.utils import get
import utils.leveling.leveling_utils as leveling_utils
import utils.server.server_utils as su

logger = logging.getLogger('SkyNet-Core.Events')

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../data/config/config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):

        channel = message.channel
        member = message.author
        nick = member.display_name
        embed = discord.Embed(title='ACHTUNG',
        description='Ein wiederholter Verstoß könnte einen Ban nach sich ziehen.',
        color=discord.Color.dark_red())

        for c in maintenance['curseWords']:
            if c in message.content:
                await message.delete()
                logger.critical(f'Curse Word was detected in a message from {member}, and the message "{message.content}" was deleted')
                embed.add_field(name=nick,
                value='Hat ein geblacklistetes Wort verwendet.',
                inline=False
                )
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            await leveling_utils.exp_gain(message)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        place = get(guild.categories, name=maintenance['tmpCatName'])

        embed = discord.Embed(title='empty', color=discord.Color.dark_grey())

        tmp_channel_name = ''

        for c in maintenance['tempChannelName']:
            tmp_channel_name += c

        for vc in place.voice_channels:
            vs = vc.voice_states
            if str(vc) == str(tmp_channel_name):
                if not vs:
                    await su.delete_voicechannel(place=place, name=vc, member='SkyNet Bot', embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        guild = after.guild
        channel = get(guild.text_channels, name='rollenverteilung')
        streamin_grole = get(guild.roles, name='Streamer:in')

        if after == streamin_grole:
            await channel.send('Bist du ein Streamer oder eine Streamerin ?')
        else:
            await channel.send(f'Spielst du {after.name} ?')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        guild = reaction.message.guild
        channel = reaction.message.channel
        vote_channel = get(guild.text_channels, name='rollenverteilung')
        content = reaction.message.content
        splitted_content = content.split(" ")
        content_role = splitted_content[2]
        role = get(guild.roles, name=content_role)

        if channel == vote_channel:
            if reaction.emoji == "👍":
                if reaction.message.content == 'Bist du ein Streamer oder eine Streamerin ?':
                    await user.add_roles(get(guild.roles, name='Streamer:in'))
                else:
                    await user.add_roles(role)
            elif reaction.emoji == "👎":
                if reaction.message.content == 'Bist du ein Streamer oder eine Streamerin ?':
                    await user.remove_roles(get(guild.roles, name='Streamer:in'))
                else:
                    await user.remove_roles(role)
            else:
                pass
        else:
            pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        embed = discord.Embed(title='Na huch!', description='Das ist leider schief gegangen!\n Versuch es doch mal mit !help', color=discord.Color.red())
        embed.add_field(name='Es lag wohl hier dran:', value=error)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))
