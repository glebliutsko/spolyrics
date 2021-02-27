from services import ServiceABC


class Genius(ServiceABC):
    NAME = 'genius.com'

    def get_text(self, track: str) -> str:
        # TODO
        return f'Text from Genius: "{track}"'
