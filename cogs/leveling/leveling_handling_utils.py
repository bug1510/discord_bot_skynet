from discord.ext import commands
from utils.file_handler import FileHandlingUtils as fhu

class LevelHandlingUtils(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def exp_gain(self, custom_user, rate):
        if self.bot.config['Leveling']:
            db_handler = self.bot.get_cog(str(self.bot.db_handler))
            try:
                custom_user.db_entry = await db_handler.get_user_exp_and_level(custom_user.guild.id, custom_user.user.id, str(custom_user.name))
                custom_user.user_lvl_exp = await self.calc_lvl(custom_user.db_entry, rate)
                await db_handler.update_user_exp(custom_user.guild.id, custom_user.user.id, custom_user.name, custom_user.user_lvl_exp)

            except Exception as e:
                self.bot.logger.warning(f'LevelingHandlingUtils | Trying to gain exp for User {custom_user.name} failed due to: {e}')
        else:
            return

    async def calc_lvl(self, db_entry, rate):
        user_lvl_exp = []
        level = db_entry[4]
        exp = db_entry[5]

        new_exp = exp + rate

        if level == self.bot.config['maxLevel']:
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
    await bot.add_cog(LevelHandlingUtils(bot))