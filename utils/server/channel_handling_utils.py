import logging
from discord.utils import get

class ChannelHandlingUtils():
    def __init__(self) -> None:
        self.logger = logging.getLogger('SkyNet-Core.Channel_Handling_Utils')

    async def create_category(self, guild, name, member, embed):
        try:
            place = await guild.create_category_channel(name=str(name))
            self.logger.info(f'Category {place} was created by {member}')
            embed.add_field(
                name= '!Success creating Category!',
                value= f'Die Kategorie {place} wurde erstellt.',
                inline=False
            )
            return place, embed

        except Exception as e:
            self.logger.warning(f'Category {place} wasnt created due to an error: {e}')
            embed.add_field(
                name= '!Failure creating Category!',
                value= f'Die Kategorie {place} konnte nicht erstellt werden. \n{e}',
                inline=False
            )
            return embed

    async def delete_category(self, place, member, embed):
        try:
            await place.delete(reason=None)

            self.logger.info(f'{member} deleted the Category {place} successfully')
            embed.add_field(
                name= '!Success deleting Category!',
                value= f'Die Kategorie {place} wurde gelöscht.',
                inline=False
            )
        except Exception as e:
            self.logger.warning(f'{member} tried to delete the Category {place} but it failed due to an error: {e}')
            embed.add_field(
                name= '!Failure deleting Category!',
                value= f'Beim löschen der Kategorie {place} ist etwas schief gegangen,\n{e}.',
                inline=False
            )
        finally:
            return embed

    async def create_textchannel(self, guild, name, place, embed):

        counter = 0
        tc = ''

        try:
            for c in name:
                tc = await guild.create_text_channel(name=c, category=place)
                counter + 1
            if counter == 1:
                self.logger.info(f'The Text Channel for {place} was created')
                embed.add_field(
                    name= '!Success creating Text Channel!',
                    value= f'Der Textkanal für {place} wurde erstellt',
                    inline=False
                )
            else:
                self.logger.info(f'The Text Channels for {place} were created')
                embed.add_field(
                    name= '!Success creating Text Channel!',
                    value= f'Der Textkanal für {place} wurde erstellt',
                    inline=False
                )
        except Exception as e:
            self.logger.warning(f'While creating the Text Channels for {place} went something wrong: {e}.')
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

    async def delete_textchannel(self, place, name, member, embed):    
        if str(name) == 'all':
            try:
                for tc in place.text_channels:
                    await tc.delete(reason=None)
                
                self.logger.info(f'{member} deleted all Text Channels from the Category {place} successfully')
                embed.add_field(
                    name= '!Success deleting Text Channels!',
                    value= f'Die Textkanäle aus {place} wurden gelöscht',
                    inline=False
                )
            except Exception as e:
                self.logger.warning(f'{member} tried to delete all Text Channels from the Category {place} but it failed due to an error: {e}')
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

                self.logger.info(f'{member} deleted Text Channel {name} from the Category {place} successfully')
                embed.add_field(
                    name= '!Success deleting Text Channel!',
                    value= f'Der Textkanal {name} in {place} wurde gelöscht.',
                    inline=False
                )
            except Exception as e:
                self.logger.warning(f'{member} tried to delete Text Channel {name} from the Category {place} but it failed due to an error: {e}')
                embed.add_field(
                    name= '!Failure deleting Text Channel',
                    value= f'Beim löschen des Textkanals {name} in {place} ist etwas schief gegangen,\n{e}.',
                    inline=False
                )
            finally:
                return embed

    async def create_voicechannel(self, guild, name, userlimit, place, embed):

        counter = 0
        vc = ''

        try:    
            for c in name:
                vc = await guild.create_voice_channel(name=c, category=place, user_limit=userlimit)
                counter = counter + 1 

            if counter == 1:
                self.logger.info(f'The Voice Channel for {place} was created')
                embed.add_field(
                    name= '!Success creating Voice Channel!',
                    value= f'Die Sprachkanal für {place} wurden erstellt.',
                    inline=False
                )

            else:
                self.logger.info(f'The Voice Channels for {place} were created')
                embed.add_field(
                    name= '!Success creating Voice Channels!',
                    value= f'Die Sprachkanäle für {place} wurden erstellt.',
                    inline=False
                )
        except Exception as e:
            self.logger.warning(f'While creating the Voice Channels for {place} went something wrong: {e}.')
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

    async def delete_voicechannel(self, place, name, member, embed):

        if str(name) == 'all':
            try:
                for vc in place.voice_channels:
                    await vc.delete(reason=None)

                self.logger.info(f'{member} deleted all Voice Channels from the Category {place} successfully')
                embed.add_field(
                    name= '!Success deleting Voice Channels!',
                    value= f'Die Sprachkanäle in {place} wurden gelöscht.',
                    inline=False
                )
            except Exception as e:
                self.logger.warning(f'{member} tried to delete all Voice Channels from the Category {place} but it failed due to an error: {e}')
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

                self.logger.info(f'{member} deleted Voice Channel {name} from the Category {place} successfully')
                embed.add_field(
                    name= '!Success deleting Voice Channel!',
                    value= f'Der Sprachkanal {name} in {place} wurde gelöscht.',
                    inline=False
                )
            except Exception as e:
                self.logger.warning(f'{member} tried to delete Voice Channel {name} from the Category {place} but it failed due to an error: {e}')
                embed.add_field(
                    name= '!Failure deleting Voice Channel',
                    value= f'Beim löschen des Sprachkanals {name} in {place} ist etwas schief gegangen,\n{e}.',
                    inline=False
                )
            finally:
                return embed




