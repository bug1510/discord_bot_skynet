import logging
from discord.utils import get
from discord.ext import commands

class InitBotFunctions(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger('SkyNet-Core.Init_Functions')

    async def init_database(self):
        community_settings = self.bot.config['CommunitySettings']

        if community_settings['MultiServerLeveling'] and not community_settings['SingleServerLeveling']:
            self.bot.load_extension('database.ms_db_handler')
        elif community_settings['SingleServerLeveling'] and not community_settings['MultiServerLeveling']:
            self.bot.load_extension('database.ss_db_handler')
        else:
            return

        if community_settings['MultiServerSync']:
            pass



    async def init_vote_roles_on(self, ctx, embed):
        
        guild = ctx.message.author.guild
        place = get(guild.categories, name=self.config['maintenanceCatName'])
        tc = get(guild.channels, name='rollenverteilung')
        
        lowestrole = get(ctx.guild.roles, name=self.config['lowestSelfGiveableRole'])
        highestrole = get(ctx.guild.roles, name=self.config['highestSelfGiveableRole'])

        if not place:
            place, embed = await chhu.create_category(guild, name=self.config['maintenanceCatName'], member='Bot', embed=embed)
            embed = await phu.set_standard_permission_for_cat(guild, place, role=guild.default_role, embed=embed)

        if not tc:
            tc, embed = await chhu.create_textchannel(guild=guild, name=['rollenverteilung'], place=place, embed=embed)
        try:
            for role in ctx.guild.roles:
                if role.position < highestrole.position and role.position > lowestrole.position:
                    msg = await tc.send(f'Möchtest du die Role {role} haben?')

                    await msg.add_reaction(emoji='👍')
                    await msg.add_reaction(emoji='👎')
        
            embed.add_field(
                name= '!Success creating Roles on Vote!',
                value= 'Die Vote Nachrichten wurden angelegt.',
                inline= False
            )

        except Exception as e:
            embed.add_field(
                name= '!Failure creating Roles on Vote!',
                value= f'Die Vote Nachrichten konnten nicht angelegt werden. \n{e}',
                inline= False
            )
        finally:
            return embed

async def setup(bot):
    await bot.add_cog(InitBotFunctions(bot))