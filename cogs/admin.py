from discord.ext import commands
from discord.utils import get
import logging
logger = logging.getLogger(__name__)

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('El-Special')

    async def game_channel_create(self, context, gamename):

        """Dieser Befehl ist administrativ und legt eine ganze Rolle ihre Kategorie 
        und eigene Channel an"""

        guild = context.message.guild
        member = context.message.author
        logger.info(str(member) + ' tried to create ' + str(gamename))
        gamerole = await guild.create_role(name=gamename)
        junior_admin = get(context.guild.roles, name='Junior Admin')
        admin = get(context.guild.roles, name='Admin')
        senior_admin = get(context.guild.roles, name='Senior Admin')
        place = await guild.create_category_channel(name='<##>' + str(gamename))

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
        
        await guild.create_text_channel(name=str(gamename) + '-talk', category=place)
        
        Sprachkanaele = ['Fraktion-I', 'Fraktion-II', 'Fraktion-III', 'Fraktion-IV', 'Group-Talk']
        
        for Kanal in Sprachkanaele:
            if Kanal.find('Group'):
                await guild.create_voice_channel(name=Kanal, category=place, user_limit=8)
            else:
                await guild.create_voice_channel(name=Kanal, category=place)

def setup(bot):
    bot.add_cog(AdminCommands(bot))