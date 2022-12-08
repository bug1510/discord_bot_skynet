import logging, discord
from discord.ext import commands
from discord.utils import get
from utils.custom_object import CustomObject as co

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('SkyNet-Core.Events')


    @commands.Cog.listener()
    async def on_message(self, message):
        deleted = False
        embed = discord.Embed(title='ACHTUNG',
        description='Ein wiederholter Verstoß könnte einen Ban nach sich ziehen.',
        color=discord.Color.dark_red())
        
        leveling_handler = await self.bot.get_cog(str(self.bot.lvl_handler))

        custom_user = co(guild=message.guild, name=message.author, embed=embed )
        custom_user.user = message.author

        for c in self.config['curseWords']:
            if c in message.content:
                await message.delete()
                deleted = True
                self.logger.critical(f'Curse Word was detected in a message from {message.author}, and the message "{message.content}" was deleted')
                embed.add_field(name=message.author,
                value='Hat ein geblacklistetes Wort verwendet.',
                inline=False
                )
                await message.channel.send(embed=embed)

        if message.author.bot:
            return
        elif deleted == True:
            return
        elif message.content.startswith('!'):
            return
        else:
            await leveling_handler.exp_gain(custom_user)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        embed = discord.Embed(title='empty', color=discord.Color.dark_grey())

        tmp_channel_name = self.bot.config['tempChannelName']
        custom_channel = co(member.guild, tmp_channel_name, embed)

        channel_manager = self.bot.get_cog('ChannelHandlingUtils')
        custom_channel.place = get(member.guild.categories, name=self.bot.config['tmpCatName'])

        for vc in custom_channel.place.voice_channels:
            vs = vc.voice_states
            if str(vc) == custom_channel.name:
                if not vs:
                    custom_channel.vc = vc
                    await channel_manager.delete_voicechannel(custom_channel)

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
        content_role = splitted_content[4]
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

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):

    #     embed = discord.Embed(title='Na huch!', description='Das ist leider schief gegangen!\n Versuch es doch mal mit !help', color=discord.Color.red())
    #     embed.add_field(name='Es lag wohl hier dran:', value=error)
    #     await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Events(bot))
