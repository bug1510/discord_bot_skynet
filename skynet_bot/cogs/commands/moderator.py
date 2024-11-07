import discord
from discord.ext import commands
from discord.utils import get
from cogs.utils.custom_object import CustomObject as co

class ModeratorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='lsrole')
    @commands.has_role("Moderator")
    async def list_role(self, ctx):
        """Dieser Befehl Listet dir die zuweisbaren Rollen auf"""
        role_manager = self.bot.get_cog('RoleHandler')
        embed = discord.Embed(title='List of Roles',description="", color=discord.Color.blue())

        embed = await role_manager.listing_role(guild=ctx.message.guild, embed=embed)

        await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    @commands.has_role("Moderator")
    async def addrole(self, ctx, roles, member=None):
        """Vergibt eine oder mehrere Rollen. Gib All an für Alle verfügbaren Rollen (Mit Komma getrennt aber ohne Leerzeichen angeben!)"""
        user = ctx.message.author.display_name
        embed = discord.Embed(
            title='Adding Roles',
            description=f'{user} hat hinzufügen von Rollen ausgelöst.',
            color=discord.Color.dark_gold()
            )
        customobject = co(guild = ctx.message.guild, name=roles, embed=embed)
        customobject.roles = []
        role_manager = self.bot.get_cog('RoleHandler')

        if member:
            customobject.member = get(customobject.guild.members, name=str(member))
        else:
            customobject.member = ctx.message.author

        self.bot.logger.info(f'AdminCommands | {user} called addrole')

        if roles == 'All':
            for r in customobject.guild.roles:
                role = get(customobject.guild.roles, name=r)
                if (await role_manager.checking_role(guild=customobject.guild, role=role)):
                    customobject.roles.append(role)
            await role_manager.adding_roles(customobject)

        elif roles.find(","):
            para = roles.split(",")
            for r in para:
                role = get(customobject.guild.roles, name=r)
                if (await role_manager.checking_role(guild=customobject.guild, role=role)):
                    customobject.roles.append(role)
            await role_manager.adding_roles(customobject)

        else:
            role = get(customobject.guild.roles, name=roles)
            if (await role_manager.checking_role(guild=customobject.guild, role=role)):
                customobject.roles.append(role)
            await role_manager.adding_roles(customobject)

        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_role("Moderator")
    async def rmrole(self, ctx, roles, member=None):
        """Entfernt eine oder mehrere Rollen. Gib All an für Alle verfügbaren Rollen (Mit Komma getrennt aber ohne Leerzeichen angeben!)"""
        user = ctx.message.author.display_name
        embed = discord.Embed(
            title='Removing Roles',
            description=f'{user} hat das entfernen von Rollen ausgelöst.',
            color=discord.Color.dark_gold()
            )
        customobject = co(guild = ctx.message.guild, name=roles, embed=embed)
        customobject.roles = []
        role_manager = self.bot.get_cog('RoleHandler')

        if member:
            customobject.member = get(customobject.guild.members, name=str(member))
        else:
            customobject.member = ctx.message.author

        self.bot.logger.info(f'AdminCommands | {user} called rmrole')

        match roles:
            case 'All':
                for r in customobject.guild.roles:
                    role = get(customobject.guild.roles, name=r)
                    if (await role_manager.checking_role(guild=customobject.guild, role=role)):
                        customobject.roles.append(role)
                await role_manager.removing_roles(customobject)

            case roles.find(","):
                para = roles.split(",")
                for r in para:
                    role = get(customobject.guild.roles, name=r)
                    if (await role_manager.checking_role(guild=customobject.guild, role=role)):
                        customobject.roles.append(role)
                await role_manager.removing_roles(customobject)

            case _:
                role = [get(customobject.guild.roles, name=roles)]
                if (await role_manager.checking_role(guild=customobject.guild, role=role)):
                    customobject.roles.append(role)
                await role_manager.removing_roles(customobject)

        await ctx.channel.send(embed=embed)

    @commands.command(name='Kettenbrief')
    @commands.has_role("Moderator")
    async def invite_group(self, ctx, group, invite_message):

        user_icon = ctx.message.author.avatar_url_as(static_format='png', size=128)
        member = ctx.message.author.display_name

        guild = ctx.message.guild
        role = get(guild.roles, name=group)

        members = role.members

        embed = discord.Embed(title=f'{member} möchte dir folgendes mitteilen:', description=invite_message, color=discord.Color.purple())
        embed.set_thumbnail(url=user_icon)

        embeds = discord.Embed(title='!Alle Nutzer haben die Nachricht erhalten!', color=discord.Color.green())

        faileduser = ''

        embedf = discord.Embed(title=f'!Folgende Nutzer haben die Nachricht leider nicht erhalten!', color=discord.Color.red())

        failed = False

        for m in members:
            try:
                c = await m.create_dm()
                await c.send(embed=embed)
            except:
                if 'Mr Meeseeks' in str(m):
                    return
                else:
                    failed = True
                    faileduser += str(m) + '\n'
        
        if failed:
            embedf.add_field(
                name='Die Nutzer waren..',
                value=faileduser,
                inline=False
            )
            
            await ctx.send(embed=embedf)

        else:
            await ctx.send(embed=embeds)

    @commands.command()
    @commands.has_role("Moderator")
    async def clear(self, ctx, number=50):
        '''Löscht eine Nummer an Nachrichten aus diesem Kanal'''

        channel = ctx.message.channel
        member = ctx.message.author
        user = ctx.message.author.display_name

        user_icon = ctx.message.author.display_avatar

        embed = discord.Embed(
            title='!ACHTUNG!',
            description=f'{number} alte Nachrichten wurden aus diesem Chat gelöscht,\nvon deinem Admin: {user}',
            color=discord.Color.dark_red())

        embed.set_thumbnail(url=user_icon)

        self.bot.logger.warning(f'{number} alte Nachrichten wurden aus diesem Chat: {channel} gelöscht, vom Admin: {member}')

        await ctx.message.delete()
        await channel.purge(limit=int(number), oldest_first=True, bulk=True)
        await ctx.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ModeratorCommands(bot))