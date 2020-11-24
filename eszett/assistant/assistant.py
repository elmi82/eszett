import logging
import os
import json
import sys
import pathlib2 as pathlib

import google.oauth2.credentials
from asyncio import Queue

from google.assistant.library import Assistant
from google.assistant.library.event import EventType


class GoogleAssistant(object):
    GOOGLE_HOME_DEVICE_NAME = "Wohnzimmer"
    CREDENTIALS = os.path.join(
        os.path.expanduser("~/.config"), "google-oauthlib-tool", "credentials.json"
    )
    DEVICE_CONFIG = os.path.join(
        os.path.expanduser("~/.config"),
        "googlesamples-assistant",
        "device_config_library.json",
    )
    PROJECT_ID = "eszett-84060"

    DEVICE_API_URL = "https://embeddedassistant.googleapis.com/v1alpha2"

    def __init__(self, playlist_queue: Queue):
        self.__logger = logging.getLogger(__name__)
        self.playlist_queue = playlist_queue

        try:
            with open(GoogleAssistant.CREDENTIALS, "r") as credentials_file:
                self.__credentials = google.oauth2.credentials.Credentials(
                    token=None, **json.load(credentials_file)
                )
        except FileNotFoundError:
            self.__logger.error("Credentials not found")
            sys.exit(1)

        self.__device_model_id = None
        self.__last_device_id = None
        try:
            with open(GoogleAssistant.DEVICE_CONFIG) as device_config_file:
                device_config = json.load(device_config_file)
                self.__device_model_id = device_config["model_id"]
                self.__last_device_id = device_config.get("last_device_id", None)
        except FileNotFoundError:
            self.__logger.error("Device configuration not found")
            sys.exit(1)

    async def handle_playlist_events(self):
        with Assistant(self.__credentials, self.__device_model_id) as assistant:
            events = assistant.start()
            assistant.set_mic_mute(True)
            self.__logger.info("GoogleAssistant is ready")

            for event in events:
                if (
                    event.type == EventType.ON_CONVERSATION_TURN_FINISHED
                    or event.type == EventType.ON_MEDIA_STATE_IDLE
                ):
                    card_details = await self.playlist_queue.get()
                    query = f"Spiel {card_details.query} im {GoogleAssistant.GOOGLE_HOME_DEVICE_NAME}"
                    self.__logger.info(f"Sending query {query}")
                    assistant.send_text_query(query)
                    self.playlist_queue.task_done()
