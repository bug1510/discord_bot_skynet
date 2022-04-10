from unicodedata import category, name
import discord, logging, os, json
from discord.utils import get

logger = logging.getLogger(__name__)

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../config.json'

permissions_file = source + '/permissions.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

perm_file = open(permissions_file)
permissions = json.load(perm_file)
perm_file.close()

async def create_category(guild, name, member, embed):

    try:
        place = await guild.create_category_channel(name=str(name))
        logger.info('Category ' + str(place) + ' was created by ' + str(member))
        embed = embed.add_field(
            name= '!Success creating Category!',
            value= 'Die Kategorie ' + str(place) + ' wurde erstellt.',
            inline=False
        )

        return place, embed

    except:
        logger.warning('Category ' + str(place) + ' wasnt created')
        embed = embed.add_field(
            name= '!Failure creating Category!',
            value= 'Die Kategorie ' + str(place) + ' konnte nicht erstellt.',
            inline=False
        )

        return embed

async def create_role(guild, name, member, embed):
    
    try:
        role = await guild.create_role(name=name)
        logger.info(str(member) + ' created category bound role ' + str(name) + ' successfully')
        embed = embed.add_field(
            name= '!Success creating Category connected Role!',
            value= 'Die Rolle ' + str(name) + ' wurde erstellt.',
            inline=False
        )

        return role, embed
    
    except:
        logger.info(str(member) + ' tried to create category bound role ' + str(name) + ' but it failed')
        embed = embed.add_field(
            name= '!Failure creating Category connected Role!',
            value= 'Die Rolle ' + str(name) + ' wurde nicht erstellt,\nbitte prüfe deine Konfiguration.',
            inline=False
        )

        return embed

async def set_standard_permission_for_cat(guild, place, role, embed):

    try:
        for r in permissions['Roles']:

            if str(r) == 'defaultRole':
                space_role = guild.default_role
            elif str(r) == 'RoleByGCC':
                space_role = get(guild.roles, name=str(role))
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
        
        logger.info('Permissions for the category ' + str(place) + ' were set')
        embed = embed.add_field(
            name= '!Success setting Permissions!',
            value= 'Die Berechtigungen für die Kategorie ' + str(place) + ' wurden gesetzt.',
            inline=False
        )
    except:
        logger.warning('Failed to set Permissions for the Categorie ' + str(place))
        embed = embed.add_field(
            name= '!Failure setting Permissions!',
            value= 'Beim setzen der Berechtigung für die Kategorie\n ' + str(place) + ' ist etwas schief gelaufen bitte überprüfe die Config.',
            inline=False
        )
    finally:
        return embed

async def create_textchannel(guild, name, place, embed):

    try:
        tc = maintenance['standardTextChannels']

        await guild.create_text_channel(name=str(name), category=place)

        for c in tc:
            await guild.create_text_channel(name=c, category=place)

        logger.info('The Text Channel for ' + str(place) + ' was created')
        embed = embed.add_field(
            name= '!Success creating Text Channels!',
            value= 'Der Textkanal für ' + str(place) + ' wurde erstellt',
            inline=False
        )

    except:
        logger.warning('While creating the Test Channel for ' + str(place) + ' went something wrong please check your server config.')
        embed = embed.add_field(
            name= '!Failure creating Text Channels!',
            value= 'Beim erstellen des Textkanals für ' + str(place) + ' ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
            inline=False
        )
    finally:
        return embed

async def create_voicechannel(guild, name, place, embed):

    try:
        if name == '0':
            vc = maintenance['standardVoiceChannels']

            for c in vc:
                userlimit = maintenance['userLimit']
                await guild.create_voice_channel(name=c, category=place, user_limit=userlimit)
            
            logger.info('The Voice Channels for ' + str(place) + ' were created')
            embed = embed.add_field(
                name= '!Success creating Voice Channels!',
                value= 'Die Sprachkanäle für ' + str(place) + ' wurden erstellt.',
                inline=False
            )
        else:
            userlimit = maintenance['userLimit']
            await guild.create_voice_channel(name=name, category=place, user_limit=userlimit)
    
    except:
        logger.warning('While creating the Voice Channels for ' + str(place) + ' went something wrong please check your server config.')
        embed = embed.add_field(
            name= '!Failure creating Voice Channels',
            value= 'Beim erstellen der Sprachkanäle für ' + str(place) + ' ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
            inline=False
        )

    finally:
        return embed

async def delete_voicechannel(place, name, member):

    try:
        for vc in place.voice_channels:
            await vc.delete(reason=None)
        
        logger.info(str(member) + ' deleted all Voice Channels from the Category ' + str(name) + ' successfully')
        embed = embed.add_field(
            name= '!Success deleting Voice Channels!',
            value= 'Die Voice Channels für ' + str(place) + ' wurden gelöscht.',
            inline=False
        )
    except:
        logger.warning(str(member) + ' tried to delete all Voice Channels from the Category ' + str(name) + ' but it failed')
        embed = embed.add_field(
            name= '!Failure deleting Voice Channels',
            value= 'Beim löschen der Voice Channels für ' + str(place) + ' ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
            inline=False
        )

async def delete_textchannel(place, name, member):    
    try:
        for tc in place.text_channels:
            await tc.delete(reason=None)
        
        logger.info(str(member) + ' deleted all Text Channels from the Category ' + str(name) + ' successfully')
        embed = embed.add_field(
            name= '!Success deleting Text Channels!',
            value= 'Die Text Channels aus ' + str(place) + ' wurden gelöscht',
            inline=False
        )
    except:
        logger.warning(str(member) + ' tried to delete all Text Channels from the Category' + str(name) + ' but it failed')
        embed = embed.add_field(
            name= '!Failure deleting Text Channels',
            value= 'Beim löschen der Text Channels für ' + str(place) + ' ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
            inline=False
        )

async def delete_category(place, name, member):

    try:
        await place.delete(reason=None)

        logger.info(str(member) + ' deleted the Category ' + str(name) + ' successfully')
        embed = embed.add_field(
            name= '!Success deleting Category!',
            value= 'Die Kategorie ' + str(place) + ' wurde gelöscht.',
            inline=False
        )
    except:
        logger.warning(str(member) + ' tried to delete the Category ' + str(name) + ' but it failed')
        embed = embed.add_field(
            name= '!Failure deleting Category!',
            value= f'Beim löschen der Kategorie {place} ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
            inline=False
        )

async def delete_role(role, name, member):

    try:
        await role.delete(reason=None)

        logger.info(f'{member} deleted the role {role} successfully')
        embed = embed.add_field(
            name= '!Success deleting Role!',
            value= f'Die Rolle {role} wurde gelöscht.',
            inline=False
        )
    except:
        logger.warning(f'{member} tried to delete the role {name} but it failed')
        embed = embed.add_field(
            name= '!Failure deleting Role!',
            value= f'Beim löschen der Rolle {role} ist etwas schief gelaufen.',
            inline=False
        )
