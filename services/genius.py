import logging
from typing import TYPE_CHECKING, Optional

from lyricsgenius import Genius as GeniusAPI

import constants
from services import ServiceABC

if TYPE_CHECKING:
    from spotify import Track


class Genius(ServiceABC):
    NAME = 'genius.com'

    API_BASE_URL = 'https://api.genius.com/'
    LYRICS_BASE_URL = 'https://genius.com/'

    def __init__(self):
        self.logger = logging.getLogger('spolyrics')

        self.api = GeniusAPI(constants.Genius.TOKEN, verbose=False)

    def get_text(self, track: 'Track') -> Optional[str]:
        track = self.api.search_song(track.title.replace(' - Bonus Track', ''), track.artists[0])
        if track is None:
            self.logger.info(f'Genius: Track not found: {track}')
            return

        self.logger.debug(f'Genius: Found track: {track.title} ({track.id})')
        return track.lyrics
