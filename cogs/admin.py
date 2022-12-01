import discord, logging
from discord.ext import commands
from discord.utils import get
from utils.bot.config_handler import ConfigHandlingUtils as cohu
from utils.bot.init_functions import InitFunctions as inf
from utils.member.role_handling_utils import RoleHandlingUtils as rhu
from utils.server.role_managing_utils import RoleManagingUtils as rmu
from utils.server.channel_handling_utils import ChannelHandlingUtils as chhu

needed_role = cohu.json_handler(filename=str('config'))

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('SkyNet-Core.AdminCommands')
        self.config = cohu.json_handler(filename=str('config'))

    @commands.command()
    @commands.has_role(needed_role['maintananceRole'])
    async def init_bot(self, ctx):
        """Initialisiert deine Konfiguration auf deinem Discord."""

        member = ctx.message.author
        user = member.display_name
        
        embed = discord.Embed(
            title='Initialisieren des Bots',
            description=f'{user} hat das initialisieren ausgelöst.',
            color=discord.Color.dark_gold()
            )

        if self.config['ServerSync'] == True:
            embed = await inf.init_server_sync(ctx, embed=embed)

        if self.config['RolesOnVote'] == True:
            embed = await inf.init_vote_roles_on(ctx, embed=embed)

        if self.config['Leveling'] == True:
            embed = await inf.init_database(ctx, embed=embed)

        if self.config['InterServerLeveling'] == True:
            embed = await inf.init_inter_server_leveling(ctx, embed=embed)

        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role(needed_role['maintananceRole'])
    async def lsrole(self, context):
        """Dieser Befehl Listet dir die zuweisbaren Rollen auf"""

        lowest = get(context.guild.roles, name='@everyone')
        highestrole = get(context.guild.roles, name='Nutzer')
        member = context.message.author
        self.logger.info(str(member) + ' called lsrole')
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
    @commands.has_role(needed_role['maintananceRole'])
    async def addrole(self, ctx, roles, member=None):
        """Vergibt eine oder mehrere Rollen. Gib All an für Alle verfügbaren Rollen (Mit Komma getrennt aber ohne Leerzeichen angeben!)"""

        guild = ctx.message.guild
        user = ctx.message.author.display_name

        if member:
            member = get(guild.members, name=str(member))
        else:
            member = ctx.message.author

        self.logger.info(str(member) + ' called addrole')

        embed = discord.Embed(
            title='Adding Roles',
            description=f'{user} hat hinzufügen von Rollen ausgelöst.',
            color=discord.Color.dark_gold()
            )

        await rhu.adding_roles(guild=guild, member=member, roles=roles, embed=embed)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role(needed_role['maintananceRole'])
    async def rmrole(self, ctx, roles, member=None):
        """Entfernt eine oder mehrere Rollen. Gib All an für Alle verfügbaren Rollen (Mit Komma getrennt aber ohne Leerzeichen angeben!)"""

        if member:
            member = member
        else:
            member = ctx.message.author

        guild = ctx.message.guild
        user = ctx.message.author.display_name
        member = ctx.message.author

        self.logger.info(str(member) + ' called rmrole')

        embed = discord.Embed(
            title='Removing Roles',
            description=f'{user} hat das entfernen von Rollen ausgelöst.',
            color=discord.Color.dark_gold()
            )

        rhu.removing_roles(guild=guild, member=member, roles=roles, embed=embed)

        await ctx.send(embed=embed)

    @commands.command(name='cspace')
    @commands.has_role(needed_role['maintananceRole'])
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

        self.logger.info(f'{member} tried to create a space {space_name}')

        embed = discord.Embed(
            title='Create Space',
            description=f'Das Erstellen wurde von {user} ausgelöst.',
            color=discord.Color.dark_gold()
        )

        embed.set_thumbnail(
            url=user_icon
        )

        place, embed = await chhu.create_category(
            guild=guild,
            name=space_name,
            member=member,
            embed=embed
        )

        role, embed = await chhu.create_role(
            guild=guild,
            name=space_name,
            member=member,
            embed=embed)

        embed = await chhu.set_standard_permission_for_cat(
            guild=guild,
            place=place,
            role=role,
            embed=embed)

        tc, embed = await chhu.create_textchannel(
            guild=guild,
            name=self.config['standardTextChannels'],
            place=place, embed=embed)

        vc, embed = await chhu.create_voicechannel(
            guild=guild,
            name=self.config['standardVoiceChannels'],
            userlimit=self.config['userLimit'],
            place=place,
            embed=embed)

        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(name='dspace')
    @commands.has_role(needed_role['maintananceRole'])
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

        self.logger.info(f'{member} tried to delete a space {space_name}')

        embed = discord.Embed(
            title='Delete Space',
            description=f'Das Löschen wurde von {user} ausgelöst.',
            color=discord.Color.dark_gold()
        )

        embed.set_thumbnail(
            url=user_icon
        )

        embed = await chhu.delete_voicechannel(
            place=place,
            name='all',
            member=member,
            embed=embed
        )

        embed = await chhu.delete_textchannel(
            place=place,
            name='all',
            member=member,
            embed=embed
        )

        embed = await chhu.delete_category(
            place=place,
            member=member,
            embed=embed
        )

        embed = await chhu.delete_role(
            role=role,
            member=member,
            embed=embed
        )

        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    @commands.has_role(needed_role['maintananceRole'])
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

        self.logger.info(f'{number} alte Nachrichten wurden aus diesem Chat gelöscht, vom Admin: {member}')

        await ctx.message.delete()
        await channel.purge(limit=int(number), oldest_first=True, bulk=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AdminCommands(bot))
