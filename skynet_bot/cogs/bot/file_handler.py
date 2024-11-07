import os, json, os.path
from discord.ext import commands

class FileHandler(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def json_handler(self, path: str, filename: str) -> json:
        try:
            file = str(path) + str(filename)
            file = open(file)
            open_file = json.load(file)
            file.close() 

            return open_file
        except Exception as e:
            self.bot.logger.critical(f'Das Laden des JSON {filename} ist aus folgendem Grund fehlgeschlagen: {e}')
    
    # def json_modifier():
    #     with open('data.json', 'r+') as f:
    #         data = json.load(f)
    #         data['id'] = 134 # <--- add `id` value.
    #         f.seek(0)        # <--- should reset file position to the beginning.
    #         json.dump(data, f, indent=4)
    #         f.truncate()     # remove remaining part

    async def cog_finder(self, path:str, extension) -> list:
        extensions = []
        for CogFile in (self.cog_listing(path=path, extensions=[])):
            if str(CogFile).endswith(extension):
                extensions.append(CogFile)
        return extensions

    async def cog_listing(self, path:str, extensions:list) -> list:
        try:
            for root, dirs, CogFiles in os.walk(path):
                for CogFile in CogFiles:
                    if CogFile.endswith('.py'):
                        root = root.replace("/", ".")
                        dirlist = root.split('.')
                        dirlist.reverse()
                        file_prefix = str(dirlist[1] + '.' + dirlist[0] + '.')
                        cog = file_prefix + CogFile[:-3]
                        extensions.append(cog)
            return extensions
        except Exception as e:
            self.bot.logger.critical(f'Das Laden des Ordner {path} ist aus folgendem Grund fehlgeschlagen: {e}')

async def setup(bot):
    await bot.add_cog(FileHandler(bot))