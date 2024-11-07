import discord
from discord.ext import commands
from discord.utils import get
from cogs.utils.custom_object import CustomObject as co

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cchannel')
    @commands.has_role("Admin")
    async def create_a_channel(self, ctx, channel_name, channel_category, channel_type, userlimit: int=None):
        user = ctx.message.author.display_name
        embed = discord.Embed(
            title='Creating a Channel',
            description=f'{user} hat einen Channel erstellen lassen',
            color=discord.Color.dark_gold()
            )
        channel_manager = self.bot.get_cog('ChannelManager')
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
        
        await ctx.send(embed=custom_channel.embed)

    @commands.command('dchannel')
    @commands.has_role("Admin")
    async def delete_a_channel(self , ctx, channel_name, channel_category, channel_type):
        user = ctx.message.author.display_name
        embed = discord.Embed(
            title='Deleting a Channel',
            description=f'{user} hat einen Channel löschen lassen',
            color=discord.Color.dark_gold()
            )
        channel_manager = self.bot.get_cog('ChannelManager')
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

        await ctx.message.send(embed=custom_channel.embed)

    @commands.command(name='cspace')
    @commands.has_role("Admin")
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
        space.userlimit = self.bot.server_settings['UserLimit']
        channel_manager = self.bot.get_cog('ChannelManager')
        role_manager = self.bot.get_cog('RoleManager')
        permission_handler = self.bot.get_cog('PermissionHandler')

        space = await channel_manager.create_category(space)

        space = await role_manager.create_role(space)

        space = await permission_handler.set_standard_permission_for_cat(space)

        space.channel = []
        for tc in self.bot.server_settings['StandardTextChannels']:
            space.channel.append(tc)
        space = await channel_manager.create_textchannel(space)

        space.channel = []
        for vc in self.bot.server_settings['StandardVoiceChannels']:
            space.channel.append(vc)
        space = await channel_manager.create_voicechannel(space)

        await ctx.send(embed=space.embed)
        await ctx.message.delete()

    @commands.command(name='dspace')
    @commands.has_role("Admin")
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

        channel_manager = self.bot.get_cog('ChannelManager')
        role_manager = self.bot.get_cog('RoleManager')
        
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

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
