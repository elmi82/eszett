import logging
import sys

from gmusicapi import Mobileclient


class Player(object):
    def __init__(self):
        self.__logger = logging.getLogger(__name__)

        self.__gmusic_client = Mobileclient(debug_logging = False)
        # self.gmusic_client.perform_oauth()
        success = self.__gmusic_client.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
        if not success:
            self.__logger.error("Login to google music failed")
            sys.exit(1)

