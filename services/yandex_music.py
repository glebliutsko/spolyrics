from typing import Optional, TYPE_CHECKING

from services import ServiceABC

if TYPE_CHECKING:
    from spotify import Track


class YandexMusic(ServiceABC):
    NAME = 'music.yandex.ru'

    def get_text(self, track: 'Track') -> Optional[str]:
        return f'Lyrics for {track.artists} - {track.title}'
