from typing import List


class CardDetails(object):
    def __init__(self, card_id: str, playlist: List[str]):
        self.card_id = card_id
        self.playlist = playlist
