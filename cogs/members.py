import discord
from discord.ext import commands
import logging
import utils.member.member_utils as mu

logger = logging.getLogger('SkyNet-Core.MemberCommands')

class MemberCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def lsrole(self, context):

    #     """Dieser Befehl Listet dir die für dich bereits verfügbaren Rollen auf"""

    #     lowest = get(context.guild.roles, name='@everyone')
    #     highestrole = get(context.guild.roles, name='Nutzer')
    #     member = context.message.author
    #     logger.info(str(member) + ' called lsrole')
    #     ListRolesField = ''

    #     for role in context.guild.roles:
    #         if role.position < highestrole.position and role.position > lowest.position:
    #             ListRolesField += str(role) + '\n'
    #         else:
    #             pass

    #     embed = discord.Embed(
    #         title='List of Gamingroles',
    #         description=ListRolesField,
    #         color=discord.Color.blue()
    #     )
    #     await context.send(embed=embed)
    #     await context.message.delete()

    @commands.command()
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

def setup(bot):
    bot.add_cog(MemberCommands(bot))