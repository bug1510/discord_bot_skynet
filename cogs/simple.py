import time,os,requests,discord,logging
import mutagen
from mutagen.mp3 import MP3
from discord.ext.commands import bot
from discord.ext import commands
from discord.utils import get

logger = logging.getLogger(__name__)
source = os.path.dirname(os.path.abspath(__file__))
class Just4Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()

    # tell a joke

    async def joke(self,ctx,language="de"):

        """Langeweile? Mr Meeseeks erzählt dir gerne ein paar Witze | Mögliche Werte für Language sind cs, fr, en, de, es, pt."""
        EmbededMessage = ''
        member = ctx.message.author
        await ctx.message.delete()
        logger.info(str(member) + ' called joke')
        logger.info('displayname : ' + str(member.display_name))
        joke_req = requests.get('https://v2.jokeapi.dev/joke/Any?lang=' + language)
        joke_payload = joke_req.json()
        if joke_req.status_code == 200:
            if joke_payload['type'] == 'twopart':
                question = joke_payload['setup']
                answer = joke_payload['delivery']
                EmbededMessage = 'Q : ' + question + '\n'
                EmbededMessage += 'A : ' + answer + '\n'
            if joke_payload['type'] == 'single':
                joke_send =  joke_payload['joke']
                EmbededMessage = joke_send
        else:
            logger.warning('use failover api')
            joke_req = requests.get("https://official-joke-api.appspot.com/jokes/programming/random")
            joke_payload = joke_req.json()
            EmbededMessage = 'Q : ' + joke_payload['setup'] + '\n'
            EmbededMessage += 'A : ' + joke_payload['punchline'] + '\n'
        
        embed = discord.Embed(title='J O K E',
                              description=EmbededMessage,
                              color=discord.Color.blue())

        file = discord.File(source + "/../img/lol.png", filename="lol.png")
        embed.set_thumbnail(url="attachment://lol.png")
        await ctx.send(file=file,embed=embed)
        await ctx.message.delete()

        
    @commands.command()
    async def cat(self,context):

        """Du willst was süßes sehen? Dann lass dir ein Kätzchen zeigen."""
        
        cat_pic = requests.get('https://cataas.com/cat?json=true')
        cat_pic_json = cat_pic.json()
        pic_url = cat_pic_json['url']
        mbed = discord.Embed(
            title='Cutie',
            description='meow',
            color=discord.Color.purple()
            )
        mbed.set_image(
            url= 'https://cataas.com/' + str(pic_url)
        )
        await context.send(embed=mbed)
        await context.message.delete()

    @commands.command()

    async def cat2(self,ctx):

        """Du willst was süßes sehen? Dann lass dir ein Kätzchen zeigen."""

        # download file
        CacheFile = source + '/../tmp/cat.jpg'
        URLFile = requests.get('http://thecatapi.com/api/images/get?format=src&type=jpg')

        with open(CacheFile,'wb') as file:
            file.write(URLFile.content)

        embed = discord.Embed(title='Random Cat',
                              color=discord.Color.blue())

        file = discord.File(CacheFile, filename="cat.png")
        embed.set_image(url="attachment://cat.png")

        await ctx.send(file=file,embed=embed)
        await ctx.message.delete()

    @commands.command()

    async def dog(self,ctx):

        """ süße Hunde gibts hier """

        dog_pic = requests.get('https://random.dog/woof.json')
        dog_pic_json = dog_pic.json()
        dog_pic_url = dog_pic_json['url']
        print(dog_pic_url)
        embed = discord.Embed(
            title='Random Dog',
            color=discord.Color.blue()
            )
        embed.set_image(
            url = dog_pic_url
        )
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()

    async def clown(self,ctx):

        """ top secret """

        CacheFile = source + '/../tmp/sound.mp3'
        URLFile = requests.get('http://api.pleaseclown.me/')
        with open(CacheFile,'wb') as file:
            file.write(URLFile.content)
        
        #############################################
        # need ffmpeg to play sound !               #
        # on windows ffmpeg must be in the path var #
        # ----------------------------------------- #
        # pip install mutagen                       #
        # pip install ffmpeg                        #
        # apt install ffmpeg
        #############################################

        voicechannel = discord.utils.get(ctx.guild.channels, name='quatschen')
        vc = await voicechannel.connect()
        vc.play(discord.FFmpegPCMAudio(CacheFile), after=lambda e: print('done', e))
        # Get Time
        mf = MP3(CacheFile)
        TrackLength = int(mf.info.length) + 1  
        time.sleep(TrackLength)
        await vc.disconnect()


        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Just4Fun(bot))