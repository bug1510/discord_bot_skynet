import json, os, logging, discord
from discord.ext import commands

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

logger = logging.getLogger(__name__)

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

def setup(bot):
    bot.add_cog(Events(bot))