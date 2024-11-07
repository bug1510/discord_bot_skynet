import discord
from discord.ext import commands
from cogs.utils.custom_object import CustomObject

class ChannelManager(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def create_category(self, customobject: CustomObject) -> CustomObject:
        try:
            customobject.place = await customobject.guild.create_category_channel(name=str(customobject.name))
            self.bot.logger.info(f'ChannelHandlingUtils | Category {customobject.place} was created')
            customobject.embed.add_field(
                name= '!Success creating Category!',
                value= f'Die Kategorie {customobject.place} wurde erstellt.',
                inline=False
            )
        except Exception as e:
            self.bot.logger.critical(f'ChannelHandlingUtils | Category {customobject.place} wasnt created due to an error: {e}')
            customobject.embed.add_field(
                name= '!Failure creating Category!',
                value= f'Die Kategorie {customobject.place} konnte nicht erstellt werden. \nüberprüfe bitte deine Server Konfiguration und Logs.',
                inline=False
            )
            customobject.embed.color = discord.Color.red()
        finally:
            return customobject
    
    async def delete_category(self, customobject: CustomObject) -> CustomObject:
        try:
            await customobject.place.delete(reason=None)

            self.bot.logger.info(f'ChannelHandlingUtils | deleted the Category {customobject.place} successfully')
            customobject.embed.add_field(
                name= '!Success deleting Category!',
                value= f'Die Kategorie {customobject.place} wurde gelöscht.',
                inline=False
            )
        except Exception as e:
            self.bot.logger.critical(f'ChannelHandlingUtils | tried to delete the Category {customobject.place} but it failed due to an error: {e}')
            customobject.embed.add_field(
                name= '!Failure deleting Category!',
                value= f'Beim löschen der Kategorie {customobject.place} ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration und Logs.',
                inline=False
            )
            customobject.embed.color = discord.Color.red()
        finally:
            return customobject

    async def create_textchannel(self, customobject: CustomObject) -> CustomObject:
        for c in customobject.channel:
            try:
                customobject.tc = await customobject.guild.create_text_channel(name=c, category=customobject.place)
                self.bot.logger.info(f'ChannelHandlingUtils | The Text Channel {c} for {customobject.place} was created')
                customobject.embed.add_field(
                    name= '!Success creating Text Channel!',
                    value= f'Der Textkanal für {customobject.place} wurde erstellt',
                    inline=False
                )
            except Exception as e:
                self.bot.logger.critical(f'ChannelHandlingUtils | While creating the Text Channel {c} for {customobject.place} went something wrong: {e}.')
                customobject.embed.add_field(
                    name= '!Failure creating Text Channel!',
                    value= f'Beim erstellen des Textkanals {c} für {customobject.place} ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration und Logs.',
                    inline=False
                )
                customobject.embed.add_field(name='Error', value=e)
                customobject.embed.color = discord.Color.red()
        return customobject

    async def delete_textchannel(self, customobject: CustomObject) -> CustomObject:
        for tc in customobject.channel:
            try:
                await tc.delete()
                self.bot.logger.info(f'ChannelHandlingUtils | deleted Text Channel {tc} from the Category {customobject.place} successfully')
                customobject.embed.add_field(
                    name= '!Success deleting Text Channel!',
                    value= f'Der Textkanal {tc} in {customobject.place} wurde gelöscht.',
                    inline=False
                )
            except Exception as e:
                self.bot.logger.critical(f'ChannelHandlingUtils | tried to delete Text Channel {tc} from the Category {customobject.place} but it failed due to an error: {e}')
                customobject.embed.add_field(
                    name= '!Failure deleting Text Channel',
                    value= f'Beim löschen des Textkanals {tc} in {customobject.place} ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration und Logs.',
                    inline=False
                )
                customobject.embed.color = discord.Color.red()
        return customobject

    async def create_voicechannel(self, customobject: CustomObject) -> CustomObject:
        for c in customobject.channel:
            try:    
                customobject.vc = await customobject.guild.create_voice_channel(name=c, category=customobject.place, user_limit=customobject.userlimit)
                self.bot.logger.info(f'ChannelHandlingUtils | The Voice Channel {c} for {customobject.place} was created')
                customobject.embed.add_field(
                    name= '!Success creating Voice Channel!',
                    value= f'Die Sprachkanal {c} für {customobject.place} wurden erstellt.',
                    inline=False
                )
            except Exception as e:
                self.bot.logger.critical(f'ChannelHandlingUtils | While creating the Voice Channel {c} for {customobject.place} went something wrong: {e}.')
                customobject.embed.add_field(
                    name= '!Failure creating Voice Channels',
                    value= f'Beim erstellen des Sprachkanals {c} für {customobject.place} ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration und Logs.',
                    inline=False
                )
                customobject.embed.add_field(name='Error', value=e)
                customobject.embed.color = discord.Color.red()
        return customobject

    async def delete_voicechannel(self, customobject: CustomObject) -> CustomObject:
        for vc in customobject.channel:
            try:
                await vc.delete()
                self.bot.logger.info(f'ChannelHandlingUtils | deleted Voice Channel {vc} from the Category {customobject.place} successfully')
                customobject.embed.add_field(
                    name= '!Success deleting Voice Channel!',
                    value= f'Der Sprachkanal {vc} in {customobject.place} wurde gelöscht.',
                    inline=False
                )
            except Exception as e:
                self.bot.logger.critical(f'ChannelHandlingUtils | tried to delete Voice Channel {vc} from the Category {customobject.place} but it failed due to an error: {e}')
                customobject.embed.add_field(
                    name= '!Failure deleting Voice Channel',
                    value= f'Beim löschen des Sprachkanals {vc} in {customobject.place} ist etwas schief gegangen,\nüberprüfe bitte deine Server Konfiguration und Logs.',
                    inline=False
                )
                customobject.embed.color = discord.Color.red()
        return customobject

async def setup(bot):
    await bot.add_cog(ChannelManager(bot))