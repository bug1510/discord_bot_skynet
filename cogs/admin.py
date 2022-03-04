import discord, os, json, sqlite3
from discord.ext import commands
from discord.utils import get
import logging
logger = logging.getLogger(__name__)

source = os.path.dirname(os.path.abspath(__file__))
config_file = source + '/../config.json'

conf = open(config_file)
maintenance = json.load(conf)
conf.close()

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='gcc')
    @commands.has_role(maintenance['maintananceRole'])

    async def game_channel_create(self, context, gamename):

        """Dieser Befehl ist administrativ und legt eine ganze Rolle ihre Kategorie und eigene Channel an"""

        guild = context.message.guild
        member = context.message.author
        logger.info(str(member) + ' tried to create category ' + str(gamename))
        junior_admin = get(context.guild.roles, name='Junior Admin')
        admin = get(context.guild.roles, name='Admin')
        senior_admin = get(context.guild.roles, name='Senior Admin')
        user = member.display_name
        embed = discord.Embed(
            title = 'GameChannelCreate',
            description = f'Das Erstellen wurde von {user} ausgelöst.',
            color = discord.Color.dark_gold()
            )

        try:
            gamerole = await guild.create_role(name=gamename)
            logger.info(str(member) + ' created category bound role ' + str(gamename) + ' successfully')
            embed = embed.add_field(
                name= '!Success creating Category connected Role!',
                value= 'Die Rolle ' + str(gamename) + ' wurde erstellt.',
                inline=False
            )
        except:
            logger.info(str(member) + ' tried to create category bound role ' + str(gamename) + ' but it failed')
            embed = embed.add_field(
                name= '!Failure creating Category connected Role!',
                value= 'Die Rolle ' + str(gamename) + ' wurde nicht erstellt,\nbitte prüfe deine Konfiguration.',
                inline=False
            )

        try:
            place = await guild.create_category_channel(name='<##>' + str(gamename))
            logger.info('Category ' + str(place) + ' was created by ' + str(member))
            embed = embed.add_field(
                name= '!Success creating Category!',
                value= 'Der Game Channel ' + str(place) + ' wurde erstellt.',
                inline=False
            )
        except:
            logger.warning('Category ' + str(place) + ' wasnt created')
            embed = embed.add_field(
                name= '!Failure creating Category!',
                value= 'Der Game Channel ' + str(place) + ' konnte nicht erstellt.',
                inline=False
            )

        try:
            await place.set_permissions(
                guild.default_role,

                view_channel=False,
                manage_channels=False,
                manage_permissions=False,
                manage_webhooks=False,
                create_instant_invite=False,
                send_messages=False,
                embed_links=False,
                attach_files=False,
                add_reactions=False,
                use_external_emojis=False,
                mention_everyone=False,
                manage_messages=False,
                read_message_history=False,
                send_tts_messages=False,
                use_slash_commands=False,
                connect=False,
                speak=False,
                stream=False,
                use_voice_activation=False,
                priority_speaker=False,
                mute_members=False,
                deafen_members=False,
                move_members=False,
                request_to_speak=False
                )
            
            await place.set_permissions(
                gamerole,

                view_channel=True,
                manage_channels=False,
                manage_permissions=False,
                manage_webhooks=False,
                create_instant_invite=False,
                send_messages=True,
                embed_links=False,
                attach_files=False,
                add_reactions=True,
                use_external_emojis=True,
                mention_everyone=False,
                manage_messages=False,
                read_message_history=True,
                send_tts_messages=True,
                use_slash_commands=False,
                connect=True,
                speak=True,
                stream=True,
                use_voice_activation=True,
                priority_speaker=False,
                mute_members=False,
                deafen_members=False,
                move_members=False,
                request_to_speak=True
                )
            
            await place.set_permissions(
                junior_admin,

                view_channel=True,
                manage_channels=False,
                manage_permissions=False,
                manage_webhooks=False,
                create_instant_invite=False,
                send_messages=True,
                embed_links=False,
                attach_files=False,
                add_reactions=True,
                use_external_emojis=True,
                mention_everyone=True,
                manage_messages=True,
                read_message_history=True,
                send_tts_messages=True,
                use_slash_commands=False,
                connect=True,
                speak=True,
                stream=True,
                use_voice_activation=True,
                priority_speaker=False,
                mute_members=True,
                deafen_members=True,
                move_members=True,
                request_to_speak=True
                )
            
            await place.set_permissions(
                admin,

                view_channel=True,
                manage_channels=False,
                manage_permissions=False,
                manage_webhooks=False,
                create_instant_invite=False,
                send_messages=True,
                embed_links=True,
                attach_files=False,
                add_reactions=True,
                use_external_emojis=True,
                mention_everyone=True,
                manage_messages=True,
                read_message_history=True,
                send_tts_messages=True,
                use_slash_commands=True,
                connect=True,
                speak=True,
                stream=True,
                use_voice_activation=True,
                priority_speaker=True,
                mute_members=True,
                deafen_members=True,
                move_members=True,
                request_to_speak=True
                )
            
            await place.set_permissions(
                senior_admin,

                view_channel=True,
                manage_channels=True,
                manage_permissions=False,
                manage_webhooks=False,
                create_instant_invite=False,
                send_messages=True,
                embed_links=True,
                attach_files=True,
                add_reactions=True,
                use_external_emojis=True,
                mention_everyone=True,
                manage_messages=True,
                read_message_history=True,
                send_tts_messages=True,
                use_slash_commands=True,
                connect=True,
                speak=True,
                stream=True,
                use_voice_activation=True,
                priority_speaker=True,
                mute_members=True,
                deafen_members=True,
                move_members=True,
                request_to_speak=True
                )

            logger.info('Permissions for the category ' + str(place) + ' were set')
            embed = embed.add_field(
                name= '!Success setting Permissions!',
                value= 'Die Berechtigungen für den Game Channel ' + str(place) + ' gesetzt.',
                inline=False
            )
        except:
            logger.warning('Failed to set Permissions for the Categorie ' + str(place))
            embed = embed.add_field(
                name= '!Failure setting Permissions!',
                value= 'Beim setzen der Berechtigung für den Game Channel\n ' + str(place) + ' ist etwas schief gelaufen bitte überprüfe die Config.',
                inline=False
            )

        try:
            tc = maintenance['standardTextChannels']

            await guild.create_text_channel(name=str(gamename), category=place)

            for c in tc:
                await guild.create_text_channel(name=c, category=place)

            logger.info('The Text Channel for ' + str(place) + ' was created')
            embed = embed.add_field(
                name= '!Success creating Text Channels!',
                value= 'Der Text Channel für ' + str(place) + ' wurde erstellt',
                inline=False
            )
        except:
            logger.warning('While creating the Test Channel for ' + str(place) + ' went something wrong please check your server config.')
            embed = embed.add_field(
                name= '!Failure creating Text Channels!',
                value= 'Beim erstellen des Text Channel für ' + str(place) + ' ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
                inline=False
            )

        try:
            vc = maintenance['standardVoiceChannels']

            for c in vc:
                userlimit = maintenance['userLimit']
                await guild.create_voice_channel(name=c, category=place, user_limit=userlimit)
            
            logger.info('The Voice Channels for ' + str(place) + ' were created')
            embed = embed.add_field(
                name= '!Success creating Voice Channels!',
                value= 'Die Voice Channels für ' + str(place) + ' wurden erstellt.',
                inline=False
            )
        except:
            logger.warning('While creating the Voice Channels for ' + str(place) + ' went something wrong please check your server config.')
            embed = embed.add_field(
                name= '!Failure creating Voice Channels',
                value= 'Beim erstellen der Voice Channels für ' + str(place) + ' ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
                inline=False
            )
            
        await context.send(embed=embed)
        await context.message.delete()
        
    @commands.command('gcd')
    @commands.has_role(maintenance['maintananceRole'])

    async def game_channel_delete(self, context, gamename):

        """Dieser Befehl ist administrativ und entfernt eine Rolle ihre Kategorie und alle Channel darin"""
        guild = context.message.guild
        member = context.message.author
        gamerole = get(guild.roles, name=gamename)
        place = get(guild.categories, name= '<##>' + str(gamename))
        user = member.display_name
        embed = discord.Embed(
            title = 'GameChannelDelete',
            description = f'Das Löschen wurde von {user} ausgelöst.',
            color = discord.Color.dark_gold()
            )
        
        try:
            for tc in place.text_channels:
                await tc.delete(reason=None)
            
            logger.info(str(member) + ' deleted all Text Channels from the Category ' + str(gamename) + ' successfully')
            embed = embed.add_field(
                name= '!Success deleting Text Channels!',
                value= 'Die Text Channels aus ' + str(place) + ' wurden gelöscht',
                inline=False
            )
        except:
            logger.warning(str(member) + ' tried to delete all Text Channels from the Category' + str(gamename) + ' but it failed')
            embed = embed.add_field(
                name= '!Failure deleting Text Channels',
                value= 'Beim löschen der Text Channels für ' + str(place) + ' ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
                inline=False
            )
        
        try:
            for vc in place.voice_channels:
                await vc.delete(reason=None)
            
            logger.info(str(member) + ' deleted all Voice Channels from the Category ' + str(gamename) + ' successfully')
            embed = embed.add_field(
                name= '!Success deleting Voice Channels!',
                value= 'Die Voice Channels für ' + str(place) + ' wurden gelöscht.',
                inline=False
            )
        except:
            logger.warning(str(member) + ' tried to delete all Voice Channels from the Category ' + str(gamename) + ' but it failed')
            embed = embed.add_field(
                name= '!Failure deleting Voice Channels',
                value= 'Beim löschen der Voice Channels für ' + str(place) + ' ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
                inline=False
            )

        try:
            await place.delete(reason=None)

            logger.info(str(member) + ' deleted the Category ' + str(gamename) + ' successfully')
            embed = embed.add_field(
                name= '!Success deleting Category!',
                value= 'Die Kategorie ' + str(place) + ' wurde gelöscht.',
                inline=False
            )
        except:
            logger.warning(str(member) + ' tried to delete the Category ' + str(gamename) + ' but it failed')
            embed = embed.add_field(
                name= '!Failure deleting Category!',
                value= 'Beim löschen der Categrory ' + str(place) + ' ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
                inline=False
            )

        try:
            await gamerole.delete(reason=None)

            logger.info(str(member) + ' deleted the role to the Category ' + str(gamename) + ' successfully')
            embed = embed.add_field(
                name= '!Success deleting Category connected Role!',
                value= 'Die zu ' + str(place) + ' gehörige Rolle wurde gelöscht.',
                inline=False
            )
        except:
            logger.warning(str(member) + ' tried to delete the role to the Category ' + str(gamename) + ' but it failed')
            embed = embed.add_field(
                name= '!Failure deleting Category connected Role!',
                value= 'Beim löschen der zu ' + str(place) + ' gehörigen Rolle ist etwas schief gelaufen.',
                inline=False
            )

        await context.send(embed=embed)
        await context.message.delete()

    @commands.command()
    @commands.has_role(maintenance['maintananceRole'])
    async def clear(self, context, number=50):
        channel = context.message.channel
        member = context.message.author
        user = context.message.author.display_name
        embed = discord.Embed(
            title='!ACHTUNG!',
            description=f'{number} alte Nachrichten wurden aus diesem Chat gelöscht,\nvon deinem Admin: {user}',
            color=discord.Color.dark_red())
            
        await context.message.delete()
        logger.info(f'{number} alte Nachrichten wurden aus diesem Chat gelöscht, vom Admin: {member}')
        await channel.purge(limit=int(number), oldest_first=True, bulk=False)
        await context.send(embed=embed)

def setup(bot):
    bot.add_cog(AdminCommands(bot))