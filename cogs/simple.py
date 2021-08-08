import time
import requests
from discord.ext import commands
class Just4Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()

    # tell a joke

    async def joke(self,ctx,language="de"):

        """Langeweile? Mr Meeseeks erzählt dir gerne ein paar Witze | Mögliche Werte für Language sind cs, fr, en, de, es, pt."""

        member = ctx.message.author
        #logging.info(str(member) + ' called joke')
        #logging.info('displayname : ' + str(member.display_name))
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
            joke_req = requests.get("https://official-joke-api.appspot.com/jokes/programming/random")
            joke_payload = joke_req.json()
            question = joke_payload['setup']
            answer = joke_payload['punchline']
            await ctx.send(question)
            time.sleep(0.5)
            await ctx.send(answer)


def setup(bot):
    bot.add_cog(Just4Fun(bot))