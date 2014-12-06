import logging
import requests
from thunderpush.messenger import Messenger

logger = logging.getLogger()


class SortingStation(object):
    """ Handles dispatching messages to Messengers. """

    _instance = None

    def __init__(self, host, token, *args, **kwargs):
        if self._instance:
            raise Exception("SortingStation already initialized.")

        self.messengers_by_apikey = {}

        self.host = host
        self.token = token

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
            payload = {'token': self.token, 'apikey': apikey}
            r = requests.post(self.host, params=payload)
            if r.status_code == 200:
                self.create_messenger(apikey, r.text)
                return self.get_messenger_by_apikey(apikey)
            else:
                return None
