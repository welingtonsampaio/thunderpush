import logging
# import requests
from pymongo import MongoClient
from thunderpush.messenger import Messenger

# try:
#     import simplejson as json
# except ImportError:
#     import json

logger = logging.getLogger()


class SortingStation(object):
    """ Handles dispatching messages to Messengers. """

    _instance = None

    def __init__(self, *args, **kwargs):
        if self._instance:
            raise Exception("SortingStation already initialized.")

        self.messengers_by_apikey = {}

        SortingStation._instance = self

    @staticmethod
    def instance():
        return SortingStation._instance

    def create_messenger(self, apikey, apisecret):
        messenger = Messenger(apikey, apisecret)

        self.messengers_by_apikey[apikey] = messenger

    def delete_messenger(self, messenger):
        del self.messengers_by_apikey[messenger.apikey]

    def get_messenger_by_apikey(self, apikey):
        return self.messengers_by_apikey.get(apikey, None)

    def get_or_create_messenger_by_apikey(self, apikey):
        messenger = self.get_messenger_by_apikey(apikey)
        if messenger:
            return messenger
        else:
            sr = StationMongo.instance()
            secret_key = sr.from_apikey(apikey)
            if secret_key:
                self.create_messenger(apikey, secret_key)
                return self.get_messenger_by_apikey(apikey)
            else:
                return None

class StationMongo:

    _instance = None

    def __init__(self, hostname, username, password, port, db, table, public, secret):
        if self._instance:
            raise Exception("StationMongo already initialized.")

        self.table = table
        self.public = public
        self.secret = secret
        if username and password:
            client = MongoClient(username+":"+password+"@"+hostname, port)
        elif username and not password:
            client = MongoClient(username+"@"+hostname, port)
        else:
            client = MongoClient(hostname, port)
        self.db = client[db]
        StationMongo._instance = self

    @staticmethod
    def instance():
        return StationMongo._instance

    def from_apikey(self, apikey):
        table = self.db[self.table]
        content = table.find_one({self.public+"": apikey})
        if not content:
            return None
        # data = json.loads(content)
        if self.secret in content:
            return content[self.secret]
        else:
            return None
