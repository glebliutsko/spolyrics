from spotify import OAuthPKCE


class Spotify:
    def __init__(self, oauth: OAuthPKCE):
        self.oauth = oauth

    # TODO
