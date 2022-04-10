import json, os, logging, discord
from discord.ext import commands
import maintenance.embed_builder as meb

logger = logging.getLogger('SkyNet-Core.Events')

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../config.json'

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
    async def on_command_error(self, ctx, error):

        embed = await meb.build_embed(title='Na huch!', description='Das ist leider schief gegangen!\n Versuch es doch mal mit !help', color=discord.Color.red())
        embed.add_field(name='Es lag wohl hier dran:', value=error)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))
