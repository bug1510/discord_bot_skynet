import discord
from discord.ext import commands
from utils.file_handler import FileHandlingUtils as fhu
from skynet_bot import configpath

needed_role = fhu.json_handler(path=configpath, filename=str('config.json'))

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='list_loaded')
    @commands.has_role(needed_role['maintananceRole'])
    async def list_loaded_cogs(self, ctx):
        """list all cogs loaded on the server"""
        embed = discord.Embed(
            title='List of Modules',
            description='Loaded',
            color=discord.Color.blue()
        )
        ListOfLoadedCogs = ['']
        for cog in self.bot.loaded_cogs:
            ListOfLoadedCogs.append(str(cog + '\n'))

        ctx.message.send(embed=embed)
        ctx.message.delete()

    @commands.command(name='list_available')
    @commands.has_role(needed_role['maintananceRole'])
    async def list_available_cogs(self, ctx):
        """Listet alle verfügbaren Module auf"""
        embed = discord.Embed(
            title='List of Modules',
            description='Available',
            color=discord.Color.blue()
        )
        cog_handler = self.bot.get_cog('CogHandler')
        embed = await cog_handler.list_available_cogs(embed)
        
        await ctx.send(embed=embed)
        await ctx.message.delete()


    @commands.command(name='load')
    @commands.has_role(needed_role['maintananceRole'])
    async def load_cog(self, ctx, extension):
        """Lädt ein Modul um ein neustart des Bots zu vermeiden."""
        member = ctx.message.author
        extensions = ['']
        extensions.append(extension)

        embed = discord.Embed(
            title='Load Modul',
            description=f'{extension}',
        )

        cog_handler = self.bot.get_cog('CogHandler')
        embed = await cog_handler.load_cogs(member=str(member), embed=embed, extensions=extensions)

        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(name='unload')
    @commands.has_role(needed_role['maintananceRole'])
    async def unload_cog(self, ctx, extension):
        """Trennt ein Modul um es ohne Impact berabeiten oder entfernen zu können."""
        member = ctx.message.author
        extensions = ['']
        extensions.append(extension)

        embed = discord.Embed(
            title='Unload Modul',
            description=f'{extension}',
        )

        cog_handler = self.bot.get_cog('CogHandler')
        embed = await cog_handler.unload_cogs(member=str(member), embed=embed, extensions=extensions)

        await ctx.send(embed=embed)
        await ctx.message.delete()
    
    @commands.command(name='reload')
    @commands.has_role(needed_role['maintananceRole'])
    async def reload_cog(self, ctx, extension):
        """Lädt ein Modul neu wenn es sich geändert haben sollte."""
        member = ctx.message.author
        extensions = ['']
        extensions.append(extension)

        embed = discord.Embed(
            title='Reload Modul',
            description=f'{extension}',
        )

        cog_handler = self.bot.get_cog('CogHandler')
        embed = await cog_handler.reload_cogs(member=str(member), embed=embed, extensions=extensions)


        await ctx.send(embed=embed)
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
