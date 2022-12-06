import logging
from discord.ext import commands
from discord.utils import get
from utils.file_handler import FileHandlingUtils as fhu

class PermissionHandlingUtils(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def set_standard_permission_for_cat(self, space):
        for r in (fhu.json_handler(path=self.bot.configpath, filename='permissions.json'))['Roles']:
            print(r)
            try:
                if str(r) == 'defaultRole':
                    space_role = space.guild.default_role
                elif str(r) == 'RoleByGCC':
                    try:
                        space_role = get(space.guild.roles, name=str(space.role))
                    except:
                        return
                else:
                    space_role = get(space.guild.roles, name=str(r))
                
                roles = (fhu.json_handler(path=self.bot.configpath, filename='permissions.json'))['Roles']
                file_role = roles[str(r)]
                print(file_role)
                await space.place.set_permissions(
                    space_role,

                    view_channel=file_role['view_channel'],
                    manage_channels=file_role['manage_channels'],
                    manage_permissions=file_role['manage_permissions'],
                    manage_webhooks=file_role['manage_webhooks'],
                    create_instant_invite=file_role['create_instant_invite'],
                    send_messages=file_role['send_messages'],
                    embed_links=file_role['embed_links'],
                    attach_files=file_role['attach_files'],
                    add_reactions=file_role['add_reactions'],
                    use_external_emojis=file_role['use_external_emojis'],
                    mention_everyone=file_role['mention_everyone'],
                    manage_messages=file_role['manage_messages'],
                    read_message_history=file_role['read_message_history'],
                    send_tts_messages=file_role['send_tts_messages'],
                    use_slash_commands=file_role['use_slash_commands'],
                    connect=file_role['connect'],
                    speak=file_role['speak'],
                    stream=file_role['stream'],
                    use_voice_activation=file_role['use_voice_activation'],
                    priority_speaker=file_role['priority_speaker'],
                    mute_members=file_role['mute_members'],
                    deafen_members=file_role['deafen_members'],
                    move_members=file_role['move_members'],
                    request_to_speak=file_role['request_to_speak']
                    )
            
                self.bot.logger.info(f'PermissionHandlingUtils | Permissions for the new category {space.place} were set')
                space.embed.add_field(
                    name= '!Success setting Permissions!',
                    value= f'Die Berechtigungen für die Kategorie {space.place} wurden gesetzt.',
                    inline=False
                )
            except Exception as e:
                self.bot.logger.critical(f'PermissionHandlingUtils | Failed to set Permissions for the Categorie {space.place} due to an error: {e}')
                space.embed.add_field(
                    name= '!Failure setting Permissions!',
                    value= f'Beim setzen der Berechtigungen für die Kategorie {space.place}\n ist etwas schief gelaufen.\n {e}',
                    inline=False
                )
            finally:
                return space

async def setup(bot):
    await bot.add_cog(PermissionHandlingUtils(bot))