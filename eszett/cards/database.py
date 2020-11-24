import logging
import os

from asyncio import Queue
from tinydb import TinyDB, Query

from eszett import resources
from eszett.cards.carddetails import CardDetails
from eszett.cards.exceptions import CardNotFoundError


class Database(object):
    DB_PATH = f"{os.path.dirname(resources.__file__)}/database.json"

    def __init__(self, card_queue: Queue, playlist_queue: Queue):
        self.__logger = logging.getLogger(__name__)
        self.__db = TinyDB(
            Database.DB_PATH, sort_keys=True, indent=4, separators=(",", ": ")
        )
        self.__card_query = Query()
        self.card_queue = card_queue
        self.playlist_queue = playlist_queue

    def get_card_details(self, card_id: str) -> CardDetails:
        results = self.__db.search(self.__card_query.id == card_id)
        if not results:
            raise CardNotFoundError

        return CardDetails(card_id, results[0].get("query"))

    async def listen(self):
        while True:
            card_id = await self.card_queue.get()

            try:
                card_details = self.get_card_details(card_id)
            except CardNotFoundError:
                self.__logger.warning(f"Card (ID: {card_id}) not found")
                pass
            else:
                self.__logger.info(f"Received Card (ID: {card_details.card_id})")
                await self.playlist_queue.put(card_details)
            finally:
                self.card_queue.task_done()
