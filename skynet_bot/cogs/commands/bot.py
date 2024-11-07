import discord, platform, psutil
from discord.ext import commands

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Bot Admin")
    async def register_server(self, ctx):
        """Initialisiert deine Konfiguration auf deinem Discord."""


        member = ctx.message.author

        embed = discord.Embed(
            title='Registrieren des Servers',
            description=f'Server wurde von {member} registriert',
            color=discord.Color.dark_gold()
            )

        # if self.bot.['ServerSync'] == True:
        #     await inf.init_server_sync(ctx, embed=embed)

        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(name='serverinfo')
    async def get_serverinfo(self, ctx):
        """ Show Server Informations """
        embed = discord.Embed(title='Serverinformations',
        description='Informations about the Backend Server',
        color=discord.Color.orange()
        )

        SystemInfoField = 'Platform : ' + platform.system() + '\n'
        SystemInfoField += 'Version  : ' + platform.version() + '\n'
        SystemInfoField += 'CPU      : ' + platform.processor()

        embed.add_field(name='System Informations',
                        value=SystemInfoField,
                        inline=False) 
        
        RamInfoField = 'Total    : ' + str(round(((psutil.virtual_memory()[0] / 1024 ) / 1024) / 1024,0)) + ' GB \n'
        RamInfoField += 'Free     : ' + str(round(((psutil.virtual_memory()[4] / 1024 ) / 1024) / 1024,0)) + ' GB'

        embed.add_field(name='Memory Informations',
                        value=RamInfoField,
                        inline=False) 

        file = discord.File(f'{self.bot.source}/data/img/confidential.png', filename='confidential.png')
        embed.set_thumbnail(url="attachment://confidential.png")

        await ctx.channel.send(file=file,embed=embed)
        await ctx.message.delete()

    @commands.command(name='list_loaded')
    @commands.has_role("Bot Admin")
    async def list_loaded_cogs(self, ctx):
        """list all cogs loaded on the server"""
        embed = discord.Embed(
            title='List of Modules',
            description='Loaded',
            color=discord.Color.blue()
        )
        try:
            ListOfLoadedCogs = ''
            for cog in self.bot.loaded_cogs:
                CogFileSplitted = cog.split('.')
                CogFileSplitted.reverse()
                ListOfLoadedCogs += (f'-{CogFileSplitted[0]}\n')
            embed.add_field(name='Following modules were found:', value=ListOfLoadedCogs)
        except Exception as e:
            self.bot.logger(f'BotCommands | Listing the loaded Modules failed due to: {e}')
            embed.add_field(name='!Error!', value=e)
            embed.color = discord.Color.red()
        finally:
            await ctx.message.channel.send(embed=embed)
            await ctx.message.delete()

    @commands.command(name='list_available')
    @commands.has_role("Bot Admin")
    async def list_available_cogs(self, ctx):
        """Listet alle verfügbaren Module auf"""
        embed = discord.Embed(
            title='List of Modules',
            description='Available',
            color=discord.Color.blue()
        )
        cog_handler = self.bot.get_cog('CogHandler')
        embed = await cog_handler.list_available_cogs(embed)
        
        await ctx.message.channel.send(embed=embed)
        await ctx.message.delete()


    @commands.command(name='load')
    @commands.has_role("Bot Admin")
    async def load_cog(self, ctx, extension):
        """Lädt ein Modul um ein neustart des Bots zu vermeiden."""
        member = ctx.message.author
        extensions = fhu.cog_finder(path=self.bot.cogpath, extension=extension)

        embed = discord.Embed(title='Load Modul', description=f'{extension}')

        cog_handler = self.bot.get_cog('CogHandler')
        embed = await cog_handler.load_cogs(member=str(member), embed=embed, extensions=extensions)

        await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @commands.command(name='unload')
    @commands.has_role("Bot Admin")
    async def unload_cog(self, ctx, extension):
        """Trennt ein Modul um es ohne Impact berabeiten oder entfernen zu können."""
        member = ctx.message.author
        extensions = fhu.cog_finder(path=self.bot.cogpath, extension=extension)

        embed = discord.Embed(title='Unload Modul',description=f'{extension}')

        cog_handler = self.bot.get_cog('CogHandler')
        embed = await cog_handler.unload_cogs(member=str(member), embed=embed, extensions=extensions)

        await ctx.channel.send(embed=embed)
        await ctx.message.delete()
    
    @commands.command(name='reload')
    @commands.has_role("Bot Admin")
    async def reload_cog(self, ctx, extension):
        """Lädt ein Modul neu wenn es sich geändert haben sollte."""
        member = ctx.message.author
        extensions = fhu.cog_finder(path=self.bot.cogpath, extension=extension)

        embed = discord.Embed(title='Reload Modul',description=f'{extension}')

        cog_handler = self.bot.get_cog('CogHandler')
        embed = await cog_handler.reload_cogs(member=str(member), embed=embed, extensions=extensions)


        await ctx.channel.send(embed=embed)
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
