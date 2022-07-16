import logging, os, json
from discord.utils import get

logger = logging.getLogger('SkyNet-Core.Server_Utils')

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../../data/config/config.json'

permissions_file = source + '/../../data/config/permissions.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

perm_file = open(permissions_file)
permissions = json.load(perm_file)
perm_file.close()

async def create_category(guild, name, member, embed):

    try:
        place = await guild.create_category_channel(name=str(name))
        logger.info(f'Category {place} was created by {member}')
        embed.add_field(
            name= '!Success creating Category!',
            value= f'Die Kategorie {place} wurde erstellt.',
            inline=False
        )

        return place, embed

    except Exception as e:
        logger.warning(f'Category {place} wasnt created due to an error: {e}')
        embed.add_field(
            name= '!Failure creating Category!',
            value= f'Die Kategorie {place} konnte nicht erstellt werden. \n{e}',
            inline=False
        )

        return embed

async def create_role(guild, name, member, embed):
    
    try:
        role = await guild.create_role(name=name)
        logger.info(f'{member} created role {name} successfully')
        embed.add_field(
            name= '!Success creating Role!',
            value= f'Die Rolle {role} wurde erstellt.',
            inline=False
        )

        return role, embed
    
    except Exception as e:
        logger.info(f'{member} tried to create role {name} but it failed due to an error: {e}')
        embed.add_field(
            name= '!Failure creating Category connected Role!',
            value= f'Die Rolle {name} wurde nicht erstellt,\n{e}.',
            inline=False
        )

        return embed

async def set_standard_permission_for_cat(guild, place, role, embed):

    try:
        for r in permissions['Roles']:

            if str(r) == 'defaultRole':
                space_role = guild.default_role
            elif str(r) == 'RoleByGCC':
                try:
                    space_role = get(guild.roles, name=str(role))
                except:
                    return
            else:
                space_role = get(guild.roles, name=str(r))
            
            roles = permissions['Roles']
            file_role = roles[str(r)]

            await place.set_permissions(
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
        
        logger.info(f'Permissions for the category {place} were set')
        embed.add_field(
            name= '!Success setting Permissions!',
            value= f'Die Berechtigungen für die Kategorie {place} wurden gesetzt.',
            inline=False
        )
    except Exception as e:
        logger.warning(f'Failed to set Permissions for the Categorie {place} due to an error: {e}')
        embed.add_field(
            name= '!Failure setting Permissions!',
            value= f'Beim setzen der Berechtigungen für die Kategorie {place}\n ist etwas schief gelaufen.\n {e}',
            inline=False
        )
    finally:
        return embed

async def create_textchannel(guild, name, place, embed):

    counter = 0
    tc = ''

    try:
        for c in name:
            tc = await guild.create_text_channel(name=c, category=place)
            counter + 1
        if counter == 1:
            logger.info(f'The Text Channel for {place} was created')
            embed.add_field(
                name= '!Success creating Text Channel!',
                value= f'Der Textkanal für {place} wurde erstellt',
                inline=False
            )
        else:
            logger.info(f'The Text Channels for {place} were created')
            embed.add_field(
                name= '!Success creating Text Channel!',
                value= f'Der Textkanal für {place} wurde erstellt',
                inline=False
            )
    except Exception as e:
        logger.warning(f'While creating the Text Channels for {place} went something wrong: {e}.')
        embed.add_field(
            name= '!Failure creating Text Channels!',
            value= f'Beim erstellen der Textkanäle für {place} ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
            inline=False
        )
        embed.add_field(
            name='Error',
            value=e
        )
    finally:
        return tc, embed

async def create_voicechannel(guild, name, userlimit, place, embed):

    counter = 0
    vc = ''

    try:    
        for c in name:
            vc = await guild.create_voice_channel(name=c, category=place, user_limit=userlimit)
            counter = counter + 1 

        if counter == 1:
            logger.info(f'The Voice Channel for {place} was created')
            embed.add_field(
                name= '!Success creating Voice Channel!',
                value= f'Die Sprachkanal für {place} wurden erstellt.',
                inline=False
            )

        else:
            logger.info(f'The Voice Channels for {place} were created')
            embed.add_field(
                name= '!Success creating Voice Channels!',
                value= f'Die Sprachkanäle für {place} wurden erstellt.',
                inline=False
            )
    except Exception as e:
        logger.warning(f'While creating the Voice Channels for {place} went something wrong: {e}.')
        embed.add_field(
            name= '!Failure creating Voice Channels',
            value= f'Beim erstellen der Sprachkanäle für {place} ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
            inline=False
        )
        embed.add_field(
            name='Error',
            value=e
        )
    finally:
        return vc, embed

async def delete_voicechannel(place, name, member, embed):

    if str(name) == 'all':
        try:
            for vc in place.voice_channels:
                await vc.delete(reason=None)

            logger.info(f'{member} deleted all Voice Channels from the Category {place} successfully')
            embed.add_field(
                name= '!Success deleting Voice Channels!',
                value= f'Die Sprachkanäle in {place} wurden gelöscht.',
                inline=False
            )
        except Exception as e:
            logger.warning(f'{member} tried to delete all Voice Channels from the Category {place} but it failed due to an error: {e}')
            embed.add_field(
                name= '!Failure deleting Voice Channels',
                value= f'Beim löschen der Sprachkanäle in {place} ist etwas schief gegangen,\n{e}.',
                inline=False
            )
        finally:
            return embed
    else:
        try:
            vc = get(place.voice_channels, name=str(name))
            await vc.delete()

            logger.info(f'{member} deleted Voice Channel {name} from the Category {place} successfully')
            embed.add_field(
                name= '!Success deleting Voice Channel!',
                value= f'Der Sprachkanal {name} in {place} wurde gelöscht.',
                inline=False
            )
        except Exception as e:
            logger.warning(f'{member} tried to delete Voice Channel {name} from the Category {place} but it failed due to an error: {e}')
            embed.add_field(
                name= '!Failure deleting Voice Channel',
                value= f'Beim löschen des Sprachkanals {name} in {place} ist etwas schief gegangen,\n{e}.',
                inline=False
            )
        finally:
            return embed

async def delete_textchannel(place, name, member, embed):    
    
    if str(name) == 'all':
        try:
            for tc in place.text_channels:
                await tc.delete(reason=None)
            
            logger.info(f'{member} deleted all Text Channels from the Category {place} successfully')
            embed.add_field(
                name= '!Success deleting Text Channels!',
                value= f'Die Textkanäle aus {place} wurden gelöscht',
                inline=False
            )
        except Exception as e:
            logger.warning(f'{member} tried to delete all Text Channels from the Category {place} but it failed due to an error: {e}')
            embed.add_field(
                name= '!Failure deleting Text Channels',
                value= f'Beim löschen der Textkanäle für {place} ist etwas schief gegangen,\n{e}.',
                inline=False
            )
        finally:
            return embed
    else:
        try:
            tc = get(place.text_channels, name=str(name))
            await tc.delete()

            logger.info(f'{member} deleted Text Channel {name} from the Category {place} successfully')
            embed.add_field(
                name= '!Success deleting Text Channel!',
                value= f'Der Textkanal {name} in {place} wurde gelöscht.',
                inline=False
            )
        except Exception as e:
            logger.warning(f'{member} tried to delete Text Channel {name} from the Category {place} but it failed due to an error: {e}')
            embed.add_field(
                name= '!Failure deleting Text Channel',
                value= f'Beim löschen des Textkanals {name} in {place} ist etwas schief gegangen,\n{e}.',
                inline=False
            )
        finally:
            return embed

async def delete_category(place, member, embed):

    try:
        await place.delete(reason=None)

        logger.info(f'{member} deleted the Category {place} successfully')
        embed.add_field(
            name= '!Success deleting Category!',
            value= f'Die Kategorie {place} wurde gelöscht.',
            inline=False
        )
    except Exception as e:
        logger.warning(f'{member} tried to delete the Category {place} but it failed due to an error: {e}')
        embed.add_field(
            name= '!Failure deleting Category!',
            value= f'Beim löschen der Kategorie {place} ist etwas schief gegangen,\n{e}.',
            inline=False
        )
    finally:
        return embed

async def delete_role(role, member, embed):

    try:
        await role.delete(reason=None)

        logger.info(f'{member} deleted the role {role} successfully')
        embed = embed.add_field(
            name= '!Success deleting Role!',
            value= f'Die Rolle {role} wurde gelöscht.',
            inline=False
        )
    except Exception as e:
        logger.warning(f'{member} tried to delete the role {role} but it failed due to an error: {e}')
        embed = embed.add_field(
            name= '!Failure deleting Role!',
            value= f'Beim löschen der Rolle {role} ist etwas schief gelaufen,\n{e}.',
            inline=False
        )
    finally:
        return embed