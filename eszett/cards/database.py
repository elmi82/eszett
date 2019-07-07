import logging
import os

from asyncio import Queue
from tinydb import TinyDB

from eszett import resources


class Database(object):
    DB_PATH = f"{os.path.dirname(resources.__file__)}/database.json"

    def __init__(self, card_queue: Queue):
        self.__logger = logging.getLogger(__name__)
        self.__db = TinyDB(Database.DB_PATH, sort_keys=True, indent=4, separators=(',', ': '))
        self.card_queue = card_queue

    async def listen(self):
        while True:
            card_id = await self.card_queue.get()
            self.__logger.info(f"Received Card with ID {card_id}")
            self.card_queue.task_done()
