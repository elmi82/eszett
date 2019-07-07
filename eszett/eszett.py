import logging
import asyncio

from eszett.cards.database import Database
from eszett.reader.reader import CardReader


async def start():
    logging.info("eszett - easy-peasy casting")

    card_queue = asyncio.Queue()
    reader = CardReader(card_queue)
    database = Database(card_queue)

    card_reader = asyncio.create_task(reader.read_cards())
    database_listener = asyncio.create_task(database.listen())
    await asyncio.gather(card_reader)
    await card_queue.join()
    database_listener.cancel()
