import os, logging
from skynet_bot import maintenance
from data.config.db_secret import myclient

logger = logging.getLogger('SkyNet-Core.Leveling_Utils')

source = os.path.dirname(os.path.abspath(__file__))

dblist = myclient.list_database_names()
if "mydatabase" in dblist:
    print("The database exists.")

