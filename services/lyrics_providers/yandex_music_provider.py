from typing import Optional, TYPE_CHECKING

import yandex_music

from services.lyrics_providers import LyricsProviderABC

if TYPE_CHECKING:
    from services.spotify import Track


class YandexMusicProvider(LyricsProviderABC):
    NAME = 'music.yandex.ru'

    def __init__(self):
        self.api = yandex_music.Client()

    def get_text(self, track: 'Track') -> Optional[str]:
        search_result = self.api.search(f'{track.artists_str()} - {track.title}').tracks
        if search_result is None:
            return

        best_track = search_result.results[0]
        supplement = best_track.get_supplement()
        if supplement.lyrics is None:
            return None

        return supplement.lyrics.full_lyrics
