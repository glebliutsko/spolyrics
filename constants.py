class Config:
    # TODO: Путь для Windows и MacOS
    # DEFAULT_CONFIG_FILE = os.path.join(os.getenv('HOME'), 'config/spolyrics/config.ini')
    DEFAULT_CONFIG_FILE = './config.ini'


class Spotify:
    CLIENT_ID = '8c2c359638fb440a9f97e771647ffcb6'
    REDIRECT_URL = 'https://open.spotify.com/'
    SCOPE = ['user-read-playback-state']
