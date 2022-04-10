import time, os, requests, discord, logging
from mutagen.mp3 import MP3
from discord.ext import commands

logger = logging.getLogger('SkyNet-Core.Sounds')

source = os.path.dirname(os.path.abspath(__file__))


class Sounds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clown(self, ctx):
        """ top secret """

        CacheFile = source + '/../tmp/sound.mp3'
        URLFile = requests.get('http://api.pleaseclown.me/')
        with open(CacheFile, 'wb') as file:
            file.write(URLFile.content)

        #############################################
        # need ffmpeg to play sound !               #
        # on windows ffmpeg must be in the path var #
        # ----------------------------------------- #
        # pip install mutagen                       #
        # pip install ffmpeg                        #
        # apt install ffmpeg                        #
        #############################################

        voicechannel = discord.utils.get(ctx.guild.channels, name='quatschen')
        vc = await voicechannel.connect()
        vc.play(discord.FFmpegPCMAudio(CacheFile),
                after=lambda e: print('done', e))
        # Get Time
        mf = MP3(CacheFile)
        TrackLength = int(mf.info.length) + 3
        time.sleep(TrackLength)
        await vc.disconnect()
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Sounds(bot))