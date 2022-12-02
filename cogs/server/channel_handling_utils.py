import logging
from discord.ext import commands
from discord.utils import get

class Space:
    def __init__(self, ctx, name: str, embed, place = None, role = None, text_channel = '', voice_channel = '') -> None:
        self.guild = ctx.message.guild
        self.name = name
        self.embed = embed
        self.place = place
        self.role = role
        self.text_channel = text_channel
        self.voice_channel = voice_channel

class ChannelHandlingUtils(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger('SkyNet-Core.Channel_Handling_Utils')

    async def create_category(self, space):
        try:
            space.place = await space.guild.create_category_channel(name=str(space.name))
            self.logger.info(f'Category {space.place} was created by {space.member}')
            space.embed.add_field(
                name= '!Success creating Category!',
                value= f'Die Kategorie {space.place} wurde erstellt.',
                inline=False
            )
            return space

        except Exception as e:
            self.logger.warning(f'Category {space.place} wasnt created due to an error: {e}')
            space.embed.add_field(
                name= '!Failure creating Category!',
                value= f'Die Kategorie {space.place} konnte nicht erstellt werden. \n{e}',
                inline=False
            )
            return space

    async def delete_category(self, space):
        try:
            await space.place.delete(reason=None)

            self.logger.info(f'{space.member} deleted the Category {space.place} successfully')
            space.embed.add_field(
                name= '!Success deleting Category!',
                value= f'Die Kategorie {space.place} wurde gelöscht.',
                inline=False
            )
        except Exception as e:
            self.logger.warning(f'{space.member} tried to delete the Category {space.place} but it failed due to an error: {e}')
            space.embed.add_field(
                name= '!Failure deleting Category!',
                value= f'Beim löschen der Kategorie {space.place} ist etwas schief gegangen,\n{e}.',
                inline=False
            )
        finally:
            return space

    async def create_textchannel(self, space):
        counter = 0
        tc = space.text_channel
        name = space.config['standardTextChannels']

        try:
            for c in name:
                tc = await space.guild.create_text_channel(name=c, category=space.place)
                counter + 1
            if counter == 1:
                self.logger.info(f'The Text Channel for {space.place} was created')
                space.embed.add_field(
                    name= '!Success creating Text Channel!',
                    value= f'Der Textkanal für {space.place} wurde erstellt',
                    inline=False
                )
            else:
                self.logger.info(f'The Text Channels for {space.place} were created')
                space.embed.add_field(
                    name= '!Success creating Text Channel!',
                    value= f'Der Textkanal für {space.place} wurde erstellt',
                    inline=False
                )
        except Exception as e:
            self.logger.warning(f'While creating the Text Channels for {space.place} went something wrong: {e}.')
            space.embed.add_field(
                name= '!Failure creating Text Channels!',
                value= f'Beim erstellen der Textkanäle für {space.place} ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
                inline=False
            )
            space.embed.add_field(
                name='Error',
                value=e
            )
        finally:
            return space

    async def delete_textchannel(self, space):    
        if str(space.channel) == 'all':
            try:
                for tc in space.place.text_channels:
                    await tc.delete(reason=None)
                
                self.logger.info(f'{space.member} deleted all Text Channels from the Category {space.place} successfully')
                space.embed.add_field(
                    name= '!Success deleting Text Channels!',
                    value= f'Die Textkanäle aus {space.place} wurden gelöscht',
                    inline=False
                )
            except Exception as e:
                self.logger.warning(f'{space.member} tried to delete all Text Channels from the Category {space.place} but it failed due to an error: {e}')
                space.embed.add_field(
                    name= '!Failure deleting Text Channels',
                    value= f'Beim löschen der Textkanäle für {space.place} ist etwas schief gegangen,\n{e}.',
                    inline=False
                )
            finally:
                return space
        else:
            try:
                tc = get(space.place.text_channels, name=str(space.channel))
                await tc.delete()

                self.logger.info(f'{space.member} deleted Text Channel {space.channel} from the Category {space.place} successfully')
                space.embed.add_field(
                    name= '!Success deleting Text Channel!',
                    value= f'Der Textkanal {space.name} in {space.place} wurde gelöscht.',
                    inline=False
                )
            except Exception as e:
                self.logger.warning(f'{space.member} tried to delete Text Channel {space.channel} from the Category {space.place} but it failed due to an error: {e}')
                space.embed.add_field(
                    name= '!Failure deleting Text Channel',
                    value= f'Beim löschen des Textkanals {space.channel} in {space.place} ist etwas schief gegangen,\n{e}.',
                    inline=False
                )
            finally:
                return space

    async def create_voicechannel(self, space):
        counter = 0
        vc = space.voice_channel
        name = space.config['standardVoiceChannels']
        userlimit = space.config['userLimit']
        
        try:    
            for c in name:
                vc = await space.guild.create_voice_channel(name=c, category=space.place, user_limit=userlimit)
                counter = counter + 1 

            if counter == 1:
                self.logger.info(f'The Voice Channel for {space.place} was created')
                space.embed.add_field(
                    name= '!Success creating Voice Channel!',
                    value= f'Die Sprachkanal für {space.place} wurden erstellt.',
                    inline=False
                )

            else:
                self.logger.info(f'The Voice Channels for {space.place} were created')
                space.embed.add_field(
                    name= '!Success creating Voice Channels!',
                    value= f'Die Sprachkanäle für {space.place} wurden erstellt.',
                    inline=False
                )
        except Exception as e:
            self.logger.warning(f'While creating the Voice Channels for {space.place} went something wrong: {e}.')
            space.embed.add_field(
                name= '!Failure creating Voice Channels',
                value= f'Beim erstellen der Sprachkanäle für {space.place} ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration.',
                inline=False
            )
            space.embed.add_field(
                name='Error',
                value=e
            )
        finally:
            return space

    async def delete_voicechannel(self, space):

        if str(space.channel) == 'all':
            try:
                for vc in space.place.voice_channels:
                    await vc.delete(reason=None)

                self.logger.info(f'{space.member} deleted all Voice Channels from the Category {space.place} successfully')
                space.embed.add_field(
                    name= '!Success deleting Voice Channels!',
                    value= f'Die Sprachkanäle in {space.place} wurden gelöscht.',
                    inline=False
                )
            except Exception as e:
                self.logger.warning(f'{space.member} tried to delete all Voice Channels from the Category {space.place} but it failed due to an error: {e}')
                space.embed.add_field(
                    name= '!Failure deleting Voice Channels',
                    value= f'Beim löschen der Sprachkanäle in {space.place} ist etwas schief gegangen,\n{e}.',
                    inline=False
                )
            finally:
                return space
        else:
            try:
                vc = get(space.place.voice_channels, name=str(space.channel))
                await vc.delete()

                self.logger.info(f'{space.member} deleted Voice Channel {space.channel} from the Category {space.place} successfully')
                space.embed.add_field(
                    name= '!Success deleting Voice Channel!',
                    value= f'Der Sprachkanal {space.channel} in {space.place} wurde gelöscht.',
                    inline=False
                )
            except Exception as e:
                self.logger.warning(f'{space.member} tried to delete Voice Channel {space.channel} from the Category {space.place} but it failed due to an error: {e}')
                space.embed.add_field(
                    name= '!Failure deleting Voice Channel',
                    value= f'Beim löschen des Sprachkanals {space.channel} in {space.place} ist etwas schief gegangen,\n{e}.',
                    inline=False
                )
            finally:
                return space

async def setup(bot):
    await bot.add_cog(ChannelHandlingUtils(bot))