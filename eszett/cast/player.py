import logging
import sys

from asyncio import Queue
from gmusicapi import Mobileclient


class Player(object):
    def __init__(self, playlist_queue: Queue):
        self.__logger = logging.getLogger(__name__)
        self.playlist_queue = playlist_queue

        self.__gmusic_client = Mobileclient(debug_logging = False)
        # self.gmusic_client.perform_oauth()
        success = self.__gmusic_client.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
        if not success:
            self.__logger.error("Login to google music failed")
            sys.exit(1)

    async def handle_playlist_events(self):
        while True:
            card_details = await self.playlist_queue.get()
            self.__logger.info(f"Received playlist {card_details.playlist}")
            self.playlist_queue.task_done()
