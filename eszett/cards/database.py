import logging

from asyncio import Queue


class Database(object):
    def __init__(self, card_queue: Queue):
        self.__logger = logging.getLogger(__name__)
        self.card_queue = card_queue

    async def listen(self):
        while True:
            card_id = await self.card_queue.get()
            self.__logger.info(f"Received Card with ID {card_id}")
            self.card_queue.task_done()
