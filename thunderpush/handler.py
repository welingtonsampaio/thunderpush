import logging
import re

from sockjs.tornado import SockJSConnection
from thunderpush.sortingstation import SortingStation

try:
    import simplejson as json
except ImportError:
    import json

logger = logging.getLogger()


class ThunderSocketHandler(SockJSConnection):
    def on_open(self, info):
        logger.debug("New connection opened.")

        # no messenger object yet, client needs issue CONNECT command first
        self.messenger = None

    def on_message(self, msg):
        logger.debug("Got message: %s" % msg)

        self.process_message(msg)

    def on_close(self):
        if self.connected:
            self.messenger.unregister_user(self)
            self.messenger = None

        logger.debug("User %s has disconnected."
            % getattr(self, "userid", None))

    def force_disconnect(self):
        self.close(9002, "Server closed the connection (intentionally).")

    def process_message(self, msg):
        """
        We assume that every client message comes in following format:
        COMMAND argument1[:argument2[:argumentX]]
        """

        tokens = msg.split(" ")

        messages = {
            'CONNECT': self.handle_connect,
            'SUBSCRIBE': self.handle_subscribe,
            'UNSUBSCRIBE': self.handle_unsubscribe
        }

        try:
            messages[tokens[0]](tokens[1])
        except (KeyError, IndexError):
            logger.warning("Received invalid message: %s." % msg)

    def handle_connect(self, args):
        if self.connected:
            logger.warning("User already connected.")
            return

        try:
            self.userid, self.apikey = args.split(":")
        except ValueError:
            logger.warning("Invalid message syntax.")
            return

        # get singleton instance of SortingStation
        ss = SortingStation.instance()

        # get and store the messenger object for given apikey
        self.messenger = ss.get_or_create_messenger_by_apikey(self.apikey)

        if self.messenger:
            self.messenger.register_user(self)
        else:
            self.close(9000, "Invalid API key.")

    def handle_subscribe(self, args):
        if not self.connected:
            logger.warning("User not connected.")

            # close the connection, the user issues commands in a wrong order
            self.close(9001, "Subscribing before connecting.")
            return

        channels = filter(None, args.split(":"))

        # not subscribe in private channel, only backend connection
        prv = re.compile("^private\-")

        for channel in channels:
            if not prv.search(channel):
                self.messenger.subscribe_user_to_channel(self, channel)

    def handle_unsubscribe(self, args):
        if not self.connected:
            logger.warning("User not connected.")

            # close the connection, the user issues commands in a wrong order
            self.close(9001, "Subscribing before connecting.")
            return

        channels = filter(None, args.split(":"))

        for channel in channels:
            self.messenger.unsubscribe_user_from_channel(self, channel)

    def close(self, code=3000, message="Go away!"):
        self.session.close(code, message)

    @property
    def connected(self):
        return bool(self.messenger)
