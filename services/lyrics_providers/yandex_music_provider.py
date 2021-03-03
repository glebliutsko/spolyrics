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
        super().__init__()

        self.api = yandex_music.Client(fetch_account_status=False)

    def _requests_lyrics(self, track: 'Track') -> Optional[str]:
        try:
            search_result = self.api.search(f'{track.artists_str()} - {track.title}').tracks
            if search_result is None:
                self.logger.info(f'YandexMusicProvider: Track not found: {track}')
                return

            track_yandex_music = search_result.results[0]
            supplement = track_yandex_music.get_supplement()
            if supplement.lyrics is None:
                self.logger.info(f'YandexMusicProvider: Lyrics for {track_yandex_music.title} '
                                 f'({track_yandex_music.id}) not found.')
                return None
        except yandex_music.exceptions.BadRequest as e:
            raise APIError(self.__class__, e)
        except yandex_music.exceptions.NetworkError as e:
            raise NetworkError(self.__class__, e)

        self.logger.debug(f'YandexMusicProvider: Found track: {track_yandex_music.title} ({track_yandex_music.id})')
        return supplement.lyrics.full_lyrics
