import discord
from discord.ext import commands
from discord.utils import get
from utils.file_handler import FileHandlingUtils as fhu
from utils.custom_object import CustomObject as co
from skynet_bot import configpath

needed_role = fhu.json_handler(path=configpath, filename=str('config.json'))

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

        #if self.bot.config['ServerSync'] == True:
        #    embed = await inf.init_server_sync(ctx, embed=embed)

        #if self.bot.config['RolesOnVote'] == True:
        #    embed = await inf.init_vote_roles_on(ctx, embed=embed)

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
        role_manager = self.bot.get_cog('RoleHandler')
        embed = discord.Embed(title='List of Roles',description=ListRolesField, color=discord.Color.blue())
        ListRolesField = ''

        embed = await role_manager.listing_role(guild=ctx.message.guild, ListRolesField=ListRolesField, embed=embed)

        await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    @commands.has_role(needed_role['maintananceRole'])
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

        match roles:
            case 'All':
                for r in customobject.guild.roles:
                    role = get(customobject.guild.roles, name=r)
                    if (role_manager.check_role(guild=customobject.guild, role=role)):
                        customobject.roles.append(role)
                role_manager.adding_roles(customobject)

            case roles.find(","):
                para = roles.split(",")
                for r in para:
                    role = get(customobject.guild.roles, name=r)
                    if (role_manager.check_role(guild=customobject.guild, role=role)):
                        customobject.roles.append(role)
                role_manager.adding_roles(customobject)

            case _:
                role = [get(customobject.guild.roles, name=roles)]
                if (role_manager.check_role(guild=customobject.guild, role=role)):
                    customobject.roles.append(role)
                role_manager.adding_roles(customobject)

        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_role(needed_role['maintananceRole'])
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
                    if (role_manager.check_role(guild=customobject.guild, role=role)):
                        customobject.roles.append(role)
                role_manager.removing_roles(customobject)

            case roles.find(","):
                para = roles.split(",")
                for r in para:
                    role = get(customobject.guild.roles, name=r)
                    if (role_manager.check_role(guild=customobject.guild, role=role)):
                        customobject.roles.append(role)
                role_manager.removing_roles(customobject)

            case _:
                role = [get(customobject.guild.roles, name=roles)]
                if (role_manager.check_role(guild=customobject.guild, role=role)):
                    customobject.roles.append(role)
                role_manager.removing_roles(customobject)

        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_role(needed_role['maintananceRole'])
    async def create_a_channel(self, ctx, channel_name, channel_category, channel_type, userlimit: int=None):
        user = ctx.message.author.display_name
        embed = discord.Embed(
            title='Creating a Channel',
            description=f'{user} hat einen Channel erstellen lassen',
            color=discord.Color.dark_gold()
            )
        channel_manager = self.bot.get_cog('ChannelHandlingUtils')
        custom_channel = co(guild=ctx.message.guild, name=str(channel_name), embed=embed)
        custom_channel.channel = [str(channel_name)]
        custom_channel.place = get(custom_channel.guild.categories, name=str(channel_category))
        custom_channel.userlimit = userlimit
        
        self.bot.logger.info(f'AdminCommands | {user} called create_a_channel with type: {channel_type}')

        match channel_type:
            case 'voice':
                custom_channel = await channel_manager.create_voicechannel(custom_channel)
                pass
            case 'text':
                custom_channel = await channel_manager.create_textchannel(custom_channel)
        
        await ctx.message.send(embed=embed)

    @commands.command()
    @commands.has_role(needed_role['maintananceRole'])
    async def delete_a_channel(self , ctx, channel_name, channel_category, channel_type):
        user = ctx.message.author.display_name
        embed = discord.Embed(
            title='Deleting a Channel',
            description=f'{user} hat einen Channel löschen lassen',
            color=discord.Color.dark_gold()
            )
        channel_manager = self.bot.get_cog('ChannelHandlingUtils')
        custom_channel = co(guild=ctx.message.guild, name=[str(channel_name)], embed=embed)
        custom_channel.place = get(custom_channel.guild.categories, name=str(channel_category))
        
        
        self.bot.logger.info(f'AdminCommands | {user} called delete_a_channel with type: {channel_type}')

        match channel_type:
            case 'voice':
                custom_channel.channel = [get(custom_channel.place.voice_channels, name=str(channel_name))]
                custom_channel = await channel_manager.delete_voicechannel(custom_channel)
            case 'text':
                custom_channel.channel = [get(custom_channel.place.text_channels, name=str(channel_name))]
                custom_channel = await channel_manager.delete_textchannel(custom_channel)

        await ctx.message.send(embed=embed)

    @commands.command(name='cspace')
    @commands.has_role(needed_role['maintananceRole'])
    async def create_space(self, ctx, space_name):
        """Legt eine Kategorie eine Rolle dazu und ihre Channel an"""
        user = ctx.message.author.display_name
        self.bot.logger.info(f'AdminCommands | {user} called create_space')
        embed = discord.Embed(
            title='Create Space',
            description=f'Das Erstellen wurde von {user} ausgelöst.',
            color=discord.Color.dark_gold()
        )
        user_icon = ctx.message.author.display_avatar
        embed.set_thumbnail(url=user_icon)
        space = co(guild=ctx.message.guild, name=space_name, embed=embed)
        space.userlimit = self.bot.config['userLimit']
        channel_manager = self.bot.get_cog('ChannelManagingUtils')
        role_manager = self.bot.get_cog('RoleManagingUtils')
        permission_handler = self.bot.get_cog('PermissionHandlingUtils')

        space = await channel_manager.create_category(space)

        space = await role_manager.create_role(space)

        space = await permission_handler.set_standard_permission_for_cat(space)

        space.channel = []
        for tc in self.bot.config['standardTextChannels']:
            space.channel.append(tc)
        space = await channel_manager.create_textchannel(space)

        space.channel = []
        for vc in self.bot.config['standardVoiceChannels']:
            space.channel.append(vc)
        space = await channel_manager.create_voicechannel(space)

        await ctx.send(embed=space.embed)
        await ctx.message.delete()

    @commands.command(name='dspace')
    @commands.has_role(needed_role['maintananceRole'])
    async def delete_space(self, ctx, space_name):
        """Löscht eine Kategorie ihre Rolle und die dazugehörigen Channel an"""
        user = ctx.message.author.display_name
        self.bot.logger.info(f'AdminCommands | {user} called delete_space')
        embed = discord.Embed(
            title='Delete Space',
            description=f'Das Löschen wurde von {user} ausgelöst.',
            color=discord.Color.dark_gold()
        )
        user_icon = ctx.message.author.display_avatar
        embed.set_thumbnail(url=user_icon)
        space = co(guild=ctx.message.guild, name=space_name, embed=embed)
        space.role = get(space.guild.roles, name=space.name)
        space.place = get(space.guild.categories,name=str(space.name))

        channel_manager = self.bot.get_cog('ChannelManagingUtils')
        role_manager = self.bot.get_cog('RoleManagingUtils')
        
        space.channel = []
        for vc in space.place.voice_channels:
            space.channel.append(vc)
        space = await channel_manager.delete_voicechannel(space)

        space.channel = []
        for tc in space.place.text_channels:
            space.channel.append(tc)      
        space = await channel_manager.delete_textchannel(space)

        space = await channel_manager.delete_category(space)

        space = await role_manager.delete_role(space)

        await ctx.send(embed=space.embed)
        await ctx.message.delete()

    # Funktioniert in momentaner Kofiguration nicht
    @commands.command()
    @commands.has_role(needed_role['maintananceRole'])
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
    await bot.add_cog(AdminCommands(bot))
