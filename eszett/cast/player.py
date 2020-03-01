import logging
import sys
from typing import List

import pychromecast
from asyncio import Queue
from gmusicapi import Mobileclient

from eszett.cast.cast_state import CastState
from eszett.cast.exceptions import PlaylistEmptyError
from eszett.cast.player_state import PlayerState


class Player(object):
    CHROMECAST_DEVICE_NAME = "Drache"

    def __init__(self, playlist_queue: Queue):
        self.__logger = logging.getLogger(__name__)
        self.playlist_queue = playlist_queue
        self.__state = PlayerState()
        self.__cast_state = CastState()

        self.__gmusic_client = Mobileclient(debug_logging=False)
        # self.gmusic_client.perform_oauth()
        success = self.__gmusic_client.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
        if not success:
            self.__logger.error("Login to google music failed")
            sys.exit(1)

        chromecasts = pychromecast.get_chromecasts()
        device = next(
            cc
            for cc in chromecasts
            if cc.device.friendly_name == Player.CHROMECAST_DEVICE_NAME
        )
        device.wait()
        self.__media_controller = device.media_controller
        self.__media_controller.register_status_listener(self)
        self.__cast_state.set_to_status(self.__media_controller.status)

    async def handle_playlist_events(self):
        while True:
            card_details = await self.playlist_queue.get()
            self.__logger.info(f"Received playlist {card_details.playlist}")
            self.start_playlist(card_details.playlist)
            self.playlist_queue.task_done()

    def new_media_status(self, status):
        # TODO handle interrupted
        self.__cast_state.update(status)

        if not self.__cast_state.has_changed:
            pass

        if not self.__state.is_current_song(status.content_id):
            pass

        if status.player_is_playing and not self.__state.started:
            self.__logger.info(f"Started playing song {self.__state.current_song}")
            self.__state.started = True

        if (
            status.idle_reason == "FINISHED"
            and status.player_is_idle
            and self.__state.started
        ):
            self.__logger.info(f"Finished playing song {self.__state.current_song}")
            self.play_next_song()

    def start_playlist(self, playlist: List[str]):
        self.__state.set_playlist(playlist)
        self.play_next_song()

    def play_next_song(self):
        try:
            current_song = self.__state.next()
            self.__logger.info(f"Next song {current_song}")
        except PlaylistEmptyError:
            self.__logger.info(f"Playlist is empty")
            pass
        else:
            self.__logger.info(f"Playing next song {current_song}")
            self.__state.current_song_url = self.__gmusic_client.get_stream_url(
                current_song
            )
            self.__media_controller.play_media(
                self.__state.current_song_url, "audio/mpeg"
            )
            self.__cast_state.set_to_status(self.__media_controller.status)
            self.__media_controller.block_until_active()
