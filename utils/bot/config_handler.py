import logging, os, json

class ConfigHandlingUtils():
    def __init__(self) -> None:
        self.logger = logging.getLogger('SkyNet-Core.Config_Handling_Utils')
        self.source = os.path.dirname(os.path.abspath(__file__))
        self.fullpath = self.source + '/../../data/'
    
    async def json_handler(self, filename: str):
        try:
            file = str(self.fullpath) + str(filename) + str('.json')

            file = open(file)
            open_file = json.load(file)
            file.close()
            return open_file
        except Exception as e:
            self.logger.critical(f'Das Laden des JSON {filename} ist aus folgendem Grund fehlgeschlagen: {e}')
    
    async def json_modifier():
        with open('data.json', 'r+') as f:
            data = json.load(f)
            data['id'] = 134 # <--- add `id` value.
            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()     # remove remaining part