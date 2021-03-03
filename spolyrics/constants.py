import os


class General:
    NAME = 'spolyrics'


class Path:
    CONFIG = f'./.data-{General.NAME}/config'
    CACHE = f'./.data-{General.NAME}/cache'

    @classmethod
    def create_directory(cls):
        for i in (cls.CONFIG, cls.CACHE):
            if not os.path.exists(i):
                os.makedirs(i)


class Spotify:
    CLIENT_ID = '8c2c359638fb440a9f97e771647ffcb6'
    REDIRECT_URL = 'http://localhost:65000/'
    SCOPE = ['user-read-playback-state']


class Genius:
    TOKEN = 'CRJslq2aEJzQQfa6inGM4HCJ37GXCfJFNo-iOQFjacnZcJvI-MMm-nXT3aUa30Z3'


if not os.getenv('DEBUG') == '1':
    if os.name == 'posix':
        _user_config_dir = os.getenv('XDG_CONFIG_HOME')
        _user_cache_dir = os.getenv('XDG_CACHE_HOME')
        if _user_config_dir is None:
            _user_config_dir = os.path.join(os.getenv('HOME'), '.config')
        if _user_cache_dir is None:
            _user_cache_dir = os.path.join(os.getenv('HOME'), '.cache')

        Path.CONFIG = os.path.join(_user_config_dir, General.NAME)
        Path.CACHE = os.path.join(_user_cache_dir, General.NAME)
    elif os.name == 'nt':
        Path.CONFIG = os.path.join(os.getenv('APPDATA'), f'{General.NAME}/config')
        Path.CACHE = os.path.join(os.getenv('APPDATA'), f'{General.NAME}/cache')
