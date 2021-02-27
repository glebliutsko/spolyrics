from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from spotify import Track


class ServiceABC:
    def get_text(self, track: 'Track') -> Optional[str]:
        raise NotImplemented
