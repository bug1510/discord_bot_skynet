from pymongo import MongoClient
import urllib.parse as up

username = up.quote_plus('root')
password = up.quote_plus('bismark1510')

myclient = MongoClient("mongodb://%s:%s@localhost:27017" % (username, password))
