from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from services.spotify import Track


class LyricsProviderABC:
    def get_text(self, track: 'Track') -> Optional[str]:
        raise NotImplemented