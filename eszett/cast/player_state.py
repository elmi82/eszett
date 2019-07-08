from collections import deque
from typing import List

from eszett.cast.exceptions import PlaylistEmptyError


class PlayerState(object):
    def __init__(self):
        self.card_id = None
        self.playlist = deque()
        self.current_song = None
        self.current_song_url = None
        self.started = False

    def set_playlist(self, playlist: List[str]):
        self.playlist = deque(playlist)
        self.playlist.rotate(1)

    def is_current_song(self, content_id: str) -> bool:
        return self.current_song == content_id

    def reset(self):
        self.current_song = None
        self.current_song_url = None
        self.started = False

    def next(self) -> str:
        self.reset()
        try:
            self.current_song = self.playlist.pop()
            return self.current_song
        except IndexError:
            self.current_song = None
            raise PlaylistEmptyError()
