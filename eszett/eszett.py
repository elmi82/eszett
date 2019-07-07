import logging
import asyncio

from eszett.reader.reader import CardReader


async def start():
    logging.info("eszett - easy-peasy casting")

    card_queue = asyncio.Queue()
    reader = CardReader(card_queue)

    card_reader = asyncio.create_task(reader.read_cards())
    await asyncio.gather(card_reader)
    await card_queue.join()
