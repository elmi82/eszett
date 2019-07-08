import logging
import asyncio

from eszett.cards.database import Database
from eszett.cast.player import Player
from eszett.reader.reader import CardReader


async def start():
    logging.info("eszett - easy-peasy casting")

    card_queue = asyncio.Queue()
    playlist_queue = asyncio.Queue()

    reader = CardReader(card_queue)
    database = Database(card_queue, playlist_queue)
    player = Player(playlist_queue)

    card_reader = asyncio.create_task(reader.read_cards())
    database_listener = asyncio.create_task(database.listen())
    player = asyncio.create_task(player.handle_playlist_events())
    await asyncio.gather(card_reader)
    await playlist_queue.join()
    player.cancel()
    await card_queue.join()
    database_listener.cancel()
