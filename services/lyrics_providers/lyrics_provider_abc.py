import logging
from typing import TYPE_CHECKING, Optional
from services.lyrics_providers import SqliteCacheLyrics

if TYPE_CHECKING:
    from services.spotify import Track


class LyricsProviderABC:
    NAME = 'ABC'

    def __init__(self):
        self.logger = logging.getLogger('spolyrics')

        self.cache = SqliteCacheLyrics()

    def _requests_lyrics(self, track: 'Track') -> Optional[str]:
        raise NotImplemented

    def get_lyrics(self, track) -> Optional[str]:
        if not self.cache.is_init:
            self.cache.init_db()

        lyrics = self.cache.get_lyrics(track, self.NAME)
        if lyrics is not None:
            return lyrics

        lyrics = self._requests_lyrics(track)
        if lyrics is not None:
            self.cache.cache_lyrics(track, lyrics, self.NAME)

        return lyrics
