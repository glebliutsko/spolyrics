from typing import TYPE_CHECKING, Optional

import requests
import requests.exceptions
from lyricsgenius import Genius as GeniusAPI

from spolyrics import constants
from spolyrics.exceptions import NetworkError, HTTPError
from spolyrics.services.lyrics_providers import LyricsProviderABC

if TYPE_CHECKING:
    from spolyrics.services.spotify import Track


class GeniusProvider(LyricsProviderABC):
    NAME = 'genius.com'

    API_BASE_URL = 'https://api.genius.com/'
    LYRICS_BASE_URL = 'https://genius.com/'

    def __init__(self):
        super().__init__()

        self.api = GeniusAPI(constants.Genius.TOKEN, verbose=False)

    def _requests_lyrics(self, track: 'Track') -> Optional[str]:
        try:
            track_genius = self.api.search_song(f'{track.title.replace(" - Bonus Track", "")} by {track.artists[0]}')
            if track_genius is None:
                self.logger.info(f'GeniusProvider: Track not found: {track_genius}')
                return

            self.logger.debug(f'GeniusProvider: Found track: {track_genius.title}')
            return track_genius.lyrics
        except requests.exceptions.HTTPError as e:
            raise HTTPError(self.__class__, e)
        except requests.exceptions.RequestException as e:
            raise NetworkError(self.__class__, e)
