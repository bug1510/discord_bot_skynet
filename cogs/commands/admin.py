import discord
from discord.ext import commands
from discord.utils import get
from utils.file_handler import FileHandlingUtils as fhu
from skynet_bot import configpath

logger = logging.getLogger('SkyNet-Core.AdminCommands')
needed_role = fhu().json_handler(filename=str('config.json'))

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

        if self.bot.config['ServerSync'] == True:
            embed = await inf.init_server_sync(ctx, embed=embed)

        if self.bot.config['RolesOnVote'] == True:
            embed = await inf.init_vote_roles_on(ctx, embed=embed)

        if self.bot.config['Leveling'] == True:
            embed = await inf.init_database(ctx, embed=embed)

        if self.bot.config['InterServerLeveling'] == True:
            embed = await inf.init_inter_server_leveling(ctx, embed=embed)

        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(name='lsrole')
    @commands.has_role(needed_role['maintananceRole'])
    async def list_srole(self, ctx):
        """Dieser Befehl Listet dir die zuweisbaren Rollen auf"""
        role_handler = self.bot.get_cog('RoleHandler')
        embed = discord.Embed(title='List of Roles',description=ListRolesField, color=discord.Color.blue())
        ListRolesField = ''

        embed = await role_handler.listing_role(guild=ctx.message.guild, ListRolesField=ListRolesField, embed=embed)

        await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    @commands.has_role(needed_role['maintananceRole'])
    async def addrole(self, ctx, roles, member=None):
        """Vergibt eine oder mehrere Rollen. Gib All an für Alle verfügbaren Rollen (Mit Komma getrennt aber ohne Leerzeichen angeben!)"""
        guild = ctx.message.guild
        user = ctx.message.author.display_name
        role_handler = self.bot.get_cog('RoleHandler')

        if member:
            member = get(guild.members, name=str(member))
        else:
            member = ctx.message.author

        self.bot.logger.info(f'AdminCommands | {member} called addrole')

        embed = discord.Embed(
            title='Adding Roles',
            description=f'{user} hat hinzufügen von Rollen ausgelöst.',
            color=discord.Color.dark_gold()
            )

        embed = await role_handler.adding_roles(guild=guild, member=member, roles=roles, embed=embed)

        await ctx.channel.send(embed=embed)

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

        logger.info(str(member) + ' called rmrole')

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

        member = ctx.message.author
        user = member.display_name

        embed = discord.Embed(
            title='Create Space',
            description=f'Das Erstellen wurde von {user} ausgelöst.',
            color=discord.Color.dark_gold()
        )
        user_icon = ctx.message.author.display_avatar
        embed.set_thumbnail(url=user_icon)
        
        space = Space(ctx, name=space_name, embed=embed)
        space.member = member

        logger.info(f'{space.member} tried to create a space {space.name}')

        space.needed_role = self.needed_role

        space = await chhu().create_category(space)

        space = await rmu().create_role(space)

        space = await phu().set_standard_permission_for_cat(space)

        space = await chhu().create_textchannel(space)

        space = await chhu().create_voicechannel(space)

        await ctx.send(embed=space.embed)
        await ctx.message.delete()

    @commands.command(name='dspace')
    @commands.has_role(needed_role['maintananceRole'])
    async def delete_space(self, ctx, space_name):
        """Löscht eine Kategorie ihre Rolle und die dazugehörigen Channel an"""

        member = ctx.message.author
        user = member.display_name

        embed = discord.Embed(
            title='Delete Space',
            description=f'Das Löschen wurde von {user} ausgelöst.',
            color=discord.Color.dark_gold()
        )
        user_icon = ctx.message.author.display_avatar
        embed.set_thumbnail(url=user_icon)

        space = Space(ctx, name=space_name, embed=embed)
        space.member = member
        space.role = get(space.guild.roles, name=space.name)
        space.place = get(space.guild.categories,name=str(space.name))
        space.channel = 'all'

        logger.info(f'{member} tried to delete a space {space.name}')

        space = await chhu.delete_voicechannel(space)

        space = await chhu.delete_textchannel(space)

        space = await chhu.delete_category(space)

        space = await rmu.delete_role(space)

        await ctx.send(embed=space.embed)
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

        logger.info(f'{number} alte Nachrichten wurden aus diesem Chat gelöscht, vom Admin: {member}')

        await ctx.message.delete()
        await channel.purge(limit=int(number), oldest_first=True, bulk=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
