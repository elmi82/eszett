import logging
import sys

import pychromecast
from asyncio import Queue
from gmusicapi import Mobileclient


class Player(object):
    CHROMECAST_DEVICE_NAME = "Büro Mini"

    def __init__(self, playlist_queue: Queue):
        self.__logger = logging.getLogger(__name__)
        self.playlist_queue = playlist_queue

        self.__gmusic_client = Mobileclient(debug_logging = False)
        # self.gmusic_client.perform_oauth()
        success = self.__gmusic_client.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
        if not success:
            self.__logger.error("Login to google music failed")
            sys.exit(1)

        chromecasts = pychromecast.get_chromecasts()
        device = next(cc for cc in chromecasts if cc.device.friendly_name == Player.CHROMECAST_DEVICE_NAME)
        device.wait()
        self.__media_controller = device.media_controller

    async def handle_playlist_events(self):
        while True:
            card_details = await self.playlist_queue.get()
            self.__logger.info(f"Received playlist {card_details.playlist}")
            self.playlist_queue.task_done()
