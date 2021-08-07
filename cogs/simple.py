import time
import requests
from discord.ext import commands


class Just4Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()

    # tell a joke
    # written by Pope

    async def joke(self, context):

        """Langeweile? Mr Meeseeks erzählt dir gerne ein paar Witze | Mokkujin"""

        member = context.message.author
        #logging.info(str(member) + ' called joke')
        jokejson = requests.get("https://v2.jokeapi.dev/joke/Any?lang=de")
        joke_payload = jokejson.json()
        if jokejson.status_code == 200:
            if joke_payload['type'] == 'twopart':
                question = joke_payload['setup']
                answer = joke_payload['delivery']
                await context.send(question)
                time.sleep(1)
                await context.send(answer)
            if joke_payload['type'] == 'single':
                joke =  joke_payload['joke']
                await context.send(joke)


def setup(bot):
    bot.add_cog(Just4Fun(bot))