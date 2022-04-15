import random, discord, ssl, logging
from discord.ext import commands
from urllib.request import urlopen
from bs4 import BeautifulSoup
from utils.maintenance.embed_builder import build_embed

logger = logging.getLogger('SkyNet-Core.NightClubCommands')

ssl._create_default_https_context = ssl._create_unverified_context

class NightClubCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(name='ihnn')
    # async def ich_hab_noch_nie(self, ctx):
    #     html = urlopen('https://ich-habe-noch-nie-online.de/')
    #     bs = BeautifulSoup(html.read(),'html.parser')
    #     ihnn = str(bs.span)
    #     await ctx.send("Ich hab noch nie " + ihnn.replace('<span id="ajaxQuestion">', "").replace("</span>", "")) #tts = True

    @commands.command(name='wop')
    async def truth_or_dare(self, ctx, arg1):
        """Spiel doch eine normale Runde Wahrheit oder Pflicht."""
        if arg1 == "p":
            html = urlopen('https://wahrheitoderpflicht.net/pflicht-teenie/')
            bs = BeautifulSoup(html.read(), 'html.parser')
            pflicht = str(bs.p.text)
            await ctx.send(ctx.author.mention + ", " + pflicht)
        else:
            html = urlopen('https://wahrheitoderpflicht.net/wahrheit-teenie/')
            bs = BeautifulSoup(html.read(), 'html.parser')
            wahrheit = str(bs.p.text)
            await ctx.send(ctx.author.mention + ", " + wahrheit)

    @commands.command(name='wop18')
    async def truth_or_dare_18(self, ctx, arg1):
        """Spiel doch eine erwachsenen Runde Wahrheit oder Pflicht."""
        if arg1 == "p":
            html = urlopen('https://wahrheitoderpflicht.net/pflicht-hot/')
            bs = BeautifulSoup(html.read(), 'html.parser')
            pflicht = str(bs.p.text)
            await ctx.send(ctx.author.mention + ", " + pflicht)
        else:
            html = urlopen('https://wahrheitoderpflicht.net/wahrheit-hot/')
            bs = BeautifulSoup(html.read(), 'html.parser')
            wahrheit = str(bs.p.text)
            await ctx.send(ctx.author.mention + ", " + wahrheit)

    @commands.command(name='bottle')
    async def flaschen_drehen(self, ctx, playernames):
        """Du möchtest Flaschen drehen? Kein Problem der MeeseeksBot macht das für dich"""
        try:
            if playernames.find(",") > 0:
                # Spieler gefunden
                para = playernames.split(",")
                win = random.choice(para)
                embed = await build_embed(title='Flasche gedreht', description='Und sie zeigt auf?:', color=discord.Color.purple())
                embed.add_field(name=f'{win}', value=':sparkles:')
            else:
                # zu wenig Spieler
                embed = await build_embed(title='Flaschen drehen', description='Das ist leider schief gegangen!', color=discord.Color.red())
                embed.add_field(name='Du bist wohl leider alleine?!', value='Such dir doch ein paar Freunde zum spielen.')
        except Exception as e:
            embed = await build_embed(title='Flaschen drehen', description='Das ist leider schief gegangen!', color=discord.Color.red())
            embed.add_field(name='Error', value=e)
            embed.add_field(name='Probier es doch mal so:', value='spin_the_bottle spieler1,spieler2,spieler3,...')
        finally:
            await ctx.send(embed=embed)

    @commands.command(name='flip')
    async def coin_flip(self, ctx):
        """Du brauchst einen Münz entscheid? Kein Thema!"""
        chance = (random.randint(1,100))
    
        if chance <= 10:
            await ctx.send(":coin:  Unglaublich! Die Münze steht auf der Seite!  :coin:")
        elif 11 <= chance <= 55:
            await ctx.send(":coin:  **Kopf!**  :coin:")
        else:
            await ctx.channel.send(":coin:  **Zahl!**  :coin:")

def setup(bot):
    bot.add_cog(NightClubCommands(bot))