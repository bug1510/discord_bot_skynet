from discord.ext import commands
from cogs.utils.custom_object import CustomObject

class LevelingHandler(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def exp_gain(self, custom_user: CustomObject, rate: int) -> None:
        db_handler = self.bot.get_cog('DBHandler')
        try:
            custom_user.db_entry = await db_handler.get_user_exp_and_level(table_name, collection_name, custom_user.guild.id, custom_user.user.id, str(custom_user.name))
            custom_user.user_lvl_exp = await self.calc_lvl(custom_user.db_entry, rate)
            await db_handler.update_user_exp(custom_user.guild.id, custom_user.user.id, custom_user.name, custom_user.user_lvl_exp)

        except Exception as e:
            self.bot.logger.warning(f'LevelHandlingUtils | Trying to gain exp for User {custom_user.name} failed due to: {e}')

    async def calc_lvl(self, db_entry: list, rate: int) -> list:
        leveling = self.bot.community_settings['Leveling']

        user_lvl_exp = []
        level = db_entry[4]
        exp = db_entry[5]

        new_exp = exp + rate

        if level == leveling['MaxLevel']:
            return
        elif level < 2:
            new_level = int((exp + rate) / (100 * 2 ** (level - 1)))
        else:
            new_level = int((exp + rate) / (100 * 2 ** (level - 2)))
        
        if new_level > level:
            new_level = new_level
            new_exp = new_exp - exp
        else:
            new_level = level

        user_lvl_exp.append(new_level)
        user_lvl_exp.append(new_exp)

        return user_lvl_exp

async def setup(bot):
    await bot.add_cog(LevelingHandler(bot))