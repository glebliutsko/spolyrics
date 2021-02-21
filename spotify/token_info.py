from dataclasses import dataclass, asdict
from datetime import datetime, timedelta


@dataclass
class TokenInfo:
    token: str
    token_type: str
    scope: str
    expires: datetime
    refresh_token: str

    @classmethod
    def parse_response(cls, token_info: dict) -> 'TokenInfo':
        return cls(
            token=token_info['access_token'],
            token_type=token_info['token_type'],
            scope=token_info['scope'],
            expires=datetime.now() + timedelta(seconds=token_info['expires_in']),
            refresh_token=token_info['refresh_token']
        )

    @classmethod
    def parse_dict(cls, token_info: dict) -> 'TokenInfo':
        token_info['expires'] = datetime.fromisoformat(token_info['expires'])
        return cls(**token_info)

    def to_dict(self) -> dict:
        token_info = asdict(self)
        token_info['expires'] = token_info['expires'].isoformat()
        return token_info

    def is_expired(self) -> bool:
        return self.expires > datetime.now()
