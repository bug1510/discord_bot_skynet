import time
import discord
from discord import colour
import requests
from discord.ext import commands
import logging
logger = logging.getLogger(__name__)

class Just4Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()

    # tell a joke

    async def joke(self,ctx,language="de"):

        """Langeweile? Mr Meeseeks erzählt dir gerne ein paar Witze | Mögliche Werte für Language sind cs, fr, en, de, es, pt."""

        member = ctx.message.author
        logger.info(str(member) + ' called joke')
        logger.info('displayname : ' + str(member.display_name))
        joke_req = requests.get('https://v2.jokeapi.dev/joke/Any?lang=' + language)
        joke_payload = joke_req.json()
        if joke_req.status_code == 200:
            if joke_payload['type'] == 'twopart':
                question = joke_payload['setup']
                answer = joke_payload['delivery']
                await ctx.send(question)
                time.sleep(0.5)
                await ctx.send(answer)
            if joke_payload['type'] == 'single':
                joke_send =  joke_payload['joke']
                await ctx.send(joke_send)
        else:
            logger.warning('use failover api')
            joke_req = requests.get("https://official-joke-api.appspot.com/jokes/programming/random")
            joke_payload = joke_req.json()
            question = joke_payload['setup']
            answer = joke_payload['punchline']
            await ctx.send(question)
            time.sleep(0.5)
            await ctx.send(answer)
    
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


def setup(bot):
    bot.add_cog(Just4Fun(bot))