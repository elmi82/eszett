import logging

from asyncio import Queue
from evdev import InputDevice, list_devices, ecodes


class CardReader(object):
    UP = 0
    DEVICE_NAME = "HXGCoLtd Keyboard"

    def __init__(self, card_queue: Queue):
        self.__logger = logging.getLogger(__name__)
        self.card_queue = card_queue
        devices = [InputDevice(path) for path in list_devices()]
        self.__device = next(
            device for device in devices if device.name == self.DEVICE_NAME
        )
        self.__card_id = ""

    async def read_cards(self):
        with self.__device.grab_context():
            self.__logger.info("Starting to read cards")

            async for event in self.__device.async_read_loop():
                if event.type == ecodes.EV_KEY and event.value == self.UP:
                    if event.code == ecodes.KEY_ENTER:
                        self.__logger.info(f"Read Card (ID: {self.__card_id})")
                        await self.card_queue.put(self.__card_id)
                        self.__card_id = ""
                    else:
                        self.__card_id += ecodes.KEY[event.code][-1:]
