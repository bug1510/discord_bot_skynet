import discord
from discord.ext import commands
from discord.utils import get
from utils.custom_object import CustomObject

class RoleHandler(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def checking_role(self, guild, role):
        highestrole = get(guild.roles, name=self.bot.server_settings['HighestSelfGiveableRole'])
        lowestrole = get(guild.roles, name=self.bot.server_settings['LowestSelfGiveableRole'])
        try:
            if role.position < highestrole.position and role.position > lowestrole.position:
                return True
            else:
                return False
        except Exception as e:
            self.bot.logger.warning(f'RoleHandler | checking the Role {role} failed due to: {e}')

    async def listing_role(self, guild, embed):
        ListRolesField = ''
        try:
            for role in guild.roles:
                if (await self.checking_role(guild=guild, role=role)):
                    ListRolesField += str(role) + '\n'
                else:
                    pass
            embed.add_field(name='Found Roles', value=ListRolesField)
        except Exception as e:
            self.bot.logger(f'RoleHandler | Listing the Roles failed due to: {e}')
            embed.color = discord.Color.red()
        finally:
            return embed

    async def adding_roles(self, customobject:CustomObject) -> CustomObject:
        for r in customobject.roles:
                try:
                    await customobject.member.add_roles(r)
                    self.bot.logger.info(f'RoleHandler | {customobject.member} was given the Role: {r}')
                    customobject.embed.add_field(name=f'Success adding role!', value=r, inline=False)
                except Exception as e:
                    self.bot.logger.warning(f'RoleHandler | While adding role {r} to {customobject.member} went something wrong: {e}.')
                    customobject.embed.add_field(
                        name= '!Failure adding Roles',
                        value= f'Beim hinzufügen der Rollen ist etwas schief gegangen,\nüberprüfe bitte deine Eingabe.',
                        inline=False
                    )
                    customobject.embed.add_field(name='Error', value=e)
                    customobject.embed.color = discord.Color.red()
        return customobject

    async def removing_roles(self, customobject: CustomObject) -> CustomObject:
        for r in customobject.roles:
            try:
                await customobject.member.remove_roles(r)
                self.bot.logger.info(f'RoleHandler | Removed {r} from {customobject.member}.')
                customobject.embed.add_field(name=f'Success removing role!', value=r, inline=False)
            except Exception as e:
                self.bot.logger.warning(f'RoleHandler | While removing roles from {customobject.member} went something wrong: {e}.')
                customobject.embed.add_field(
                    name= '!Failure removing Roles',
                    value= f'Beim entfernen der Rollen ist etwas schief gegangen,\nüberprüfe bitte deine Eingabe.',
                    inline=False
                )
                customobject.embed.add_field(name='Error', value=e)
                customobject.embed.color = discord.Color.red()
        return customobject       

    async def init_vote_roles_on(self, ctx, embed):
        channel_manager = self.bot.get_cog('ChannelManagingUtils')
        permission_handler = self.bot.get_cog('PermissionHandlingUtils')
        role_manager = self.bot.get_cog('RoleHandler')
        
        server_settings = self.config['Serversettings']

        custom_channel = CustomObject(guild=ctx.message.guild, name=server_settings['TempCatName'], embed=embed)
        custom_channel.place = get(custom_channel.guild.categories, name=server_settings['TempCatName'])
        channel_name = server_settings['TempChannelName']
        channel_name = channel_name[0]
        custom_channel.channel = get(custom_channel.guild.channels, name=str(channel_name))

        if not custom_channel.place:
            custom_channel = await channel_manager.create_category(custom_channel)
            custom_channel.role = custom_channel.guild.default_role
            custom_channel = await permission_handler.set_standard_permission_for_cat(custom_channel)

        if not custom_channel.channel:
            custom_channel.channel = str(channel_name)
            custom_channel = await channel_manager.create_textchannel(custom_channel)
        try:
            for role in ctx.guild.roles:
                if (role_manager.check_role(guild=custom_channel.guild, role=role)):
                    msg = await custom_channel.channel.send(f'Möchtest du die Role {role} haben?')

                    await msg.add_reaction(emoji='👍')
                    await msg.add_reaction(emoji='👎')
        
            embed.add_field(
                name= '!Success creating Roles on Vote!',
                value= 'Die Vote Nachrichten wurden angelegt.',
                inline= False
            )

        except Exception as e:
            embed.add_field(
                name= '!Failure creating Roles on Vote!',
                value= f'Die Vote Nachrichten konnten nicht angelegt werden. \n{e}',
                inline= False
            )
        finally:
            return embed

async def setup(bot):
    await bot.add_cog(RoleHandler(bot))