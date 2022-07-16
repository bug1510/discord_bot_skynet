import discord
import os
import json
import logging
from discord.ext import commands
from discord.utils import get
import utils.server.server_utils as su
import utils.member.member_utils as mu
import utils.bot.init_functions as inf

logger = logging.getLogger('SkyNet-Core.AdminCommands')

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../data/config/config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(maintenance['maintananceRole'])
    async def init_bot(self, ctx):

        if maintenance['ServerSync'] == True:
            await inf.init_server_sync()

        if maintenance['RolesOnVote'] == True:
            await inf.init_vote_roles_on(ctx)

        if maintenance['Leveling'] == True:
            await inf.init_leveling_db(ctx)

        if maintenance['InterServerLeveling'] == True:
            await inf.init_inter_server_leveling()

    @commands.command()
    @commands.has_role(maintenance['maintananceRole'])
    async def lsrole(self, context):

        """Dieser Befehl Listet dir die für dich bereits verfügbaren Rollen auf"""

        lowest = get(context.guild.roles, name='@everyone')
        highestrole = get(context.guild.roles, name='Nutzer')
        member = context.message.author
        logger.info(str(member) + ' called lsrole')
        ListRolesField = ''

        for role in context.guild.roles:
            if role.position < highestrole.position and role.position > lowest.position:
                ListRolesField += str(role) + '\n'
            else:
                pass

        embed = discord.Embed(
            title='List of Gamingroles',
            description=ListRolesField,
            color=discord.Color.blue()
        )
        await context.send(embed=embed)
        await context.message.delete()

    @commands.command()
    @commands.has_role(maintenance['maintananceRole'])
    async def addrole(self, ctx, roles, member=None):

        """Vergibt eine oder mehrere Rollen. Gib All an für Alle verfügbaren Rollen (Mit Komma getrennt aber ohne Leerzeichen angeben!)"""

        if member:
            member = member
        else:
            member = ctx.message.author

        guild = ctx.message.guild
        user = ctx.message.author.display_name

        logger.info(str(member) + ' called addrole')

        embed = discord.Embed(
            title='Adding Roles',
            description=f'{user} hat hinzufügen von Rollen ausgelöst.',
            color=discord.Color.dark_gold()
            )

        mu.adding_roles(guild=guild, member=member, roles=roles, embed=embed)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role(maintenance['maintananceRole'])
    async def rmrole(self, ctx, roles, member=None):

        """Entfernt eine oder mehrere Rollen. Gib All an für Alle verfügbaren Rollen (Mit Komma getrennt aber ohne Leerzeichen angeben!)"""

        if member:
            member = member
        else:
            member = ctx.message.author

        guild = ctx.message.guild
        user = ctx.message.author.display_name
        member = ctx.message.author

        logger.info(str(member) + ' called rmrole')

        embed = discord.Embed(
            title='Removing Roles',
            description=f'{user} hat das entfernen von Rollen ausgelöst.',
            color=discord.Color.dark_gold()
            )

        mu.removing_roles(guild=guild, member=member, roles=roles, embed=embed)

        await ctx.send(embed=embed)

    @commands.command(name='cspace')
    @commands.has_role(maintenance['maintananceRole'])
    async def create_space(self, ctx, space_name):
        """Legt eine Kategorie eine Rolle dazu und ihre Channel an"""

        guild = ctx.message.guild
        member = ctx.message.author
        tc = ''
        vc = ''
        user = member.display_name

        user_icon = ctx.message.author.avatar_url_as(
            static_format='png',
            size=128
        )

        logger.info(f'{member} tried to create a space {space_name}')

        embed = discord.Embed(
            title='Create Space',
            description=f'Das Erstellen wurde von {user} ausgelöst.',
            color=discord.Color.dark_gold()
        )

        embed.set_thumbnail(
            url=user_icon
        )

        place, embed = await su.create_category(
            guild=guild,
            name=space_name,
            member=member,
            embed=embed
        )

        role, embed = await su.create_role(
            guild=guild,
            name=space_name,
            member=member,
            embed=embed)

        embed = await su.set_standard_permission_for_cat(
            guild=guild,
            place=place,
            role=role,
            embed=embed)

        tc, embed = await su.create_textchannel(
            guild=guild,
            name=maintenance['standardTextChannels'],
            place=place, embed=embed)

        vc, embed = await su.create_voicechannel(
            guild=guild,
            name=maintenance['standardVoiceChannels'],
            userlimit=maintenance['userLimit'],
            place=place,
            embed=embed)

        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(name='dspace')
    @commands.has_role(maintenance['maintananceRole'])
    async def delete_space(self, ctx, space_name):
        """Löscht eine Kategorie ihre Rolle und die dazugehörigen Channel an"""

        guild = ctx.message.guild
        member = ctx.message.author
        user = member.display_name

        role = get(
            guild.roles,
            name=space_name
        )

        place = get(
            guild.categories,
            name=str(space_name)
        )

        user_icon = ctx.message.author.avatar_url_as(
            static_format='png',
            size=128
        )

        logger.info(f'{member} tried to delete a space {space_name}')

        embed = discord.Embed(
            title='Delete Space',
            description=f'Das Löschen wurde von {user} ausgelöst.',
            color=discord.Color.dark_gold()
        )

        embed.set_thumbnail(
            url=user_icon
        )

        embed = await su.delete_voicechannel(
            place=place,
            name='all',
            member=member,
            embed=embed
        )

        embed = await su.delete_textchannel(
            place=place,
            name='all',
            member=member,
            embed=embed
        )

        embed = await su.delete_category(
            place=place,
            member=member,
            embed=embed
        )

        embed = await su.delete_role(
            role=role,
            member=member,
            embed=embed
        )

        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    @commands.has_role(maintenance['maintananceRole'])
    async def clear(self, ctx, number=50):
        '''Löscht eine Nummer an Nachrichten aus diesem Kanal'''

        channel = ctx.message.channel
        member = ctx.message.author
        user = ctx.message.author.display_name

        user_icon = ctx.message.author.avatar_url_as(
            static_format='png',
            size=128
        )

        embed = discord.Embed(
            title='!ACHTUNG!',
            description=f'{number} alte Nachrichten wurden aus diesem Chat gelöscht,\nvon deinem Admin: {user}',
            color=discord.Color.dark_red())

        embed.set_thumbnail(
            url=user_icon
        )

        logger.info(f'{number} alte Nachrichten wurden aus diesem Chat gelöscht, vom Admin: {member}')

        await ctx.message.delete()
        await channel.purge(limit=int(number), oldest_first=True, bulk=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AdminCommands(bot))
