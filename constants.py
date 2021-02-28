class Config:
    # TODO: Путь для Windows и MacOS
    # DEFAULT_CONFIG_FILE = os.path.join(os.getenv('HOME'), 'config/spolyrics/config.ini')
    DEFAULT_CONFIG_FILE = './config.ini'
    DEFAULT_DIRECTORY_SAVE_AUTH = './'


class Spotify:
    CLIENT_ID = '8c2c359638fb440a9f97e771647ffcb6'
    REDIRECT_URL = 'http://localhost:65000/'
    SCOPE = ['user-read-playback-state']


class Genius:
    TOKEN = 'CRJslq2aEJzQQfa6inGM4HCJ37GXCfJFNo-iOQFjacnZcJvI-MMm-nXT3aUa30Z3'
