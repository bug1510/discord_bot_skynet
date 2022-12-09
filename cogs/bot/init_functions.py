import logging
from discord.utils import get
from discord.ext import commands
from utils.file_handler import FileHandlingUtils as fhu

class InitFunctions(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.logger = logging.getLogger('SkyNet-Core.Init_Functions')

    async def register_server(self):
        pass

    async def init_database(self, ctx):
        db_handler = self.bot.get_cog(self.bot.db_handler)

    async def init_inter_server_leveling(self, ctx, embed):
        embed.add_field(
        name= '!Information Inter-Server-Leveling!',
        value= 'Inter-Server-Leveling is not implemented yet',
        inline= False
    )
        return embed
    commands.command()
    @commands.check()
    async def init_server_sync(self, ctx, embed):

        embed.add_field(
        name= '!Information on Multi-Server-Sync!',
        value= 'Multi-Server-Sync is not implemented yet',
        inline= False
    )
        return embed

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
    await bot.add_cog(InitFunctions(bot))