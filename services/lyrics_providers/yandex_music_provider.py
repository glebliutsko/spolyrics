from typing import Optional, TYPE_CHECKING

import yandex_music
import yandex_music.exceptions

from exceptions import NetworkError, APIError
from services.lyrics_providers import LyricsProviderABC

if TYPE_CHECKING:
    from services.spotify import Track


class YandexMusicProvider(LyricsProviderABC):
    NAME = 'music.yandex.ru'

    def __init__(self):
        self.api = yandex_music.Client(fetch_account_status=False)

    def get_text(self, track: 'Track') -> Optional[str]:
        try:
            search_result = self.api.search(f'{track.artists_str()} - {track.title}').tracks
            if search_result is None:
                return

            best_track = search_result.results[0]
            supplement = best_track.get_supplement()
            if supplement.lyrics is None:
                return None
        except yandex_music.exceptions.BadRequest as e:
            raise APIError(self.__class__, e)
        except yandex_music.exceptions.NetworkError as e:
            raise NetworkError(self.__class__, e)

        return supplement.lyrics.full_lyrics
