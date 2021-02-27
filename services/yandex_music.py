from services import ServiceABC


class YandexMusic(ServiceABC):
    NAME = 'music.yandex.ru'

    def get_text(self, track: str) -> str:
        # TODO
        return f'Text from Yandex Music: "{track}"\n'
