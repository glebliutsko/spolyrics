from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spolyrics.services.spotify import Track


class CacheLyricsABC:
    def get_lyrics(self, track: 'Track', provider: str) -> str:
        raise NotImplemented

    def cache_lyrics(self, track: 'Track', lyrics: str, provider: str) -> str:
        raise NotImplemented
