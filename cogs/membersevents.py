import json, os, logging, discord
from discord.utils import get
from discord.ext import commands

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

logger = logging.getLogger(__name__)

class MembersEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def init_vote_roles_on(self, ctx):
        guild = ctx.message.author.guild
        channel = get(guild.channels, name='rollenverteilung')
        lowest = get(ctx.guild.roles, name='@everyone')
        highestrole = get(ctx.guild.roles, name=maintenance['highestSelfGiveableRole'])
        streamin_grole = get(guild.roles, name='Streamer:in')

        if not channel:
            channel = await guild.create_text_channel(name='rollenverteilung')

        for role in ctx.guild.roles:
            if role.position < highestrole.position and role.position > lowest.position:
                if role == streamin_grole:
                    await channel.send('Bist du ein Streamer oder eine Streamerin ?')
                else:
                    await channel.send(f'Spielst du {role} ?')

        await ctx.message.delete()

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

def setup(bot):
    bot.add_cog(MembersEvents(bot))