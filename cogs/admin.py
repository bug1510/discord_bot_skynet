from discord import channel
import discord
from discord.ext import commands
from discord.utils import get
import logging
logger = logging.getLogger(__name__)

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='gcc')
    @commands.has_role('El-Special')

    async def game_channel_create(self, context, gamename):

        """Dieser Befehl ist administrativ und legt eine ganze Rolle ihre Kategorie und eigene Channel an"""

        guild = context.message.guild
        member = context.message.author
        logger.info(str(member) + ' tried to create category ' + str(gamename))
        gamerole = await guild.create_role(name=gamename)
        junior_admin = get(context.guild.roles, name='Junior Admin')
        admin = get(context.guild.roles, name='Admin')
        senior_admin = get(context.guild.roles, name='Senior Admin')
        
        try:
            place = await guild.create_category_channel(name='<##>' + str(gamename))

            logger.info('Category ' + str(gamename) + ' was created by ' + str(member))

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

            logger.info('Permission for the category ' + str(gamename) + ' was set')
            await context.send('Der Game Channel ' + str(gamename) + ' wurde erstellt und die Berechtigungen wurden gesetzt.')
        except:
            logger.warning('Failed to create category ' + str(gamename) + ' and/or setting Permission')
            await context.send('Beim erstellen vom Game Channel ' + str(gamename) + ' etwas schief gelaufen bitte überprüfe deine Angaben und probiere es dann nochmal.')

        try:
            await guild.create_text_channel(name=str(gamename) + '-talk', category=place)
        
            vc = ['Fraktion-I', 'Fraktion-II', 'Fraktion-III', 'Fraktion-IV', 'Group-Talk']
        
            for c in vc:
                if c.find('Group'):
                    await guild.create_voice_channel(name=c, category=place, user_limit=8)
                else:
                    await guild.create_voice_channel(name=c, category=place)
            logger.info('The Voice and Text Channels for ' + str(place) + ' were created')
            await context.send('Alle Channels für ' + str(place) + ' wurden erstellt')
        except:
            logger.warning('While creating the Channels for ' + str(place) + ' went something wrong please check input or config.')
            await context.send('Beim erstellen der Channels für ' + str(place) + ' ist etwas schief gegangen, überprüfe bitte deine Angaben oder die Konfiguration.')
        await context.message.delete()
        
    @commands.command('gcd')
    @commands.has_role('El-Special')

    async def game_channel_delete(self, context, gamename):

        """Dieser Befehl ist administrativ und entfernt eine Rolle ihre Kategorie und alle Channel darin"""
        guild = context.message.guild
        member = context.message.author
        gamerole = get(guild.roles, name=gamename)
        place = get(guild.categories, name= '<##>' + str(gamename))
        
        try:
            for tc in place.text_channels:
                await tc.delete(reason=None)

            for vc in place.voice_channels:
                await vc.delete(reason=None)

            await place.delete(reason=None)
            await gamerole.delete(reason=None)
            
            logger.warning(str(member) + ' deleted ' + str(gamename) + ' successfully')
            await context.send('Der Abschnitt ' + str(place) + ' wurde erfogreich von deinem Sever gelöscht.')

        except:
            logger.warning(str(member) + ' tried to delete ' + str(gamename) + ' but it failed')
            await context.send('Da ist wohl etwas schief gelaufen überprüfe ob du alles richtig geschrieben hast!')
        await context.message.delete()

    @commands.command()
    @commands.has_role('El-Special')
    async def clear(self, context, number):
        channel = context.message.channel
        admin = context.message.author
        embed = discord.Embed(
            title='!ACHTUNG!',
            description=f'{number} alte Nachrichten wurden aus diesem Chat von deinem Admin: {admin} gelöscht',
            color=discord.Color.dark_red())

        await channel.purge(limit=int(number), oldest_first=True, bulk=False)
        await context.send(embed=embed)
        await context.message.delete()



def setup(bot):
    bot.add_cog(AdminCommands(bot))