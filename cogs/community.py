import discord, random, time
from discord.ext import commands
from discord.utils import get
import sqlite3, json, os
from leveling.lvl import exp_gain, get_rank

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

class CommunityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='leveling_on')
    @commands.is_owner()
    async def init_leveling_db(self, ctx):
        '''Initialisiert das Leveling auf deinem Server. Also viel Spaß!'''
        guild_id = ctx.message.author.guild.id
        con = sqlite3.connect(f'{guild_id}.db')
        cur = con.cursor()
        cur.execute("""Create Table IF NOT EXISTS leveling
        (dc_user_nick text, dc_user_id integer, tw_user_nick text, tw_user_id integer, level integer NOT NULL DEFAULT 1, exp integer NOT NULL DEFAULT 0)""")
        con.commit()
        con.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            await exp_gain(message)

    @commands.command(name='rank')
    async def rank(self, ctx):
        '''Gibt dir eine genaue Übersicht über dein Level und deine Erfahrungspunkte.'''
        guild_id = ctx.message.author.guild.id
        user_nick = ctx.message.author.display_name
        embed =discord.Embed(title=f'{user_nick}´s Rank Card', color=discord.Color.blurple())

        if os.path.exists(f'{str(guild_id)}.db'):
            user_data = await get_rank(ctx)

            user_level = user_data[4]
            user_exp = user_data[5]

            embed.add_field(name='Level', value=user_level, inline=True)
            embed.add_field(name='Erfahrungspunkte', value=user_exp, inline=True)

            await ctx.send(embed=embed)
        else:
            return

    @commands.command(name='tcc')
    async def create_temp_channel(self, ctx):
        '''Erstellt dir und deinen Freunden einen Temporären Raum.'''
        guild = ctx.message.guild
        member = ctx.message.author
        tmp_cat_name = 'Temp-Channels'
        category = get(guild.categories, name=tmp_cat_name)
        r = random.randint(1, 10000000)


        if not category:
            category = await guild.create_category_channel(name=tmp_cat_name, position=0)
        userlimit = maintenance['userLimit']
        tmp_channel = await guild.create_voice_channel(name='tmp-channel' + str(r), category=category, user_limit=userlimit)

        await member.move_to(tmp_channel)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        category = get(guild.categories, name='Temp-Channels')
        for vc in category.voice_channels:
            vs = vc.voice_states
            if not vs:
                await vc.delete()

def setup(bot):
    bot.add_cog(CommunityCommands(bot))