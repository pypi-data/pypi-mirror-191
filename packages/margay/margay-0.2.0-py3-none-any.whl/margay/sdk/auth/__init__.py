import socket
from datetime import datetime, timedelta, timezone

import jwt


class JWTAuth:
    encoder = jwt.encode
    decoder = jwt.decode
    algorithm = "HS256"

    class InvalidToken(Exception):
        pass

    def __init__(self, secret: str):
        self.secret = secret

    def issue_token(self, client: str) -> str:
        return self.encoder(
            self.get_claims(client), self.secret, algorithm=self.algorithm
        )

    def verify_token(self, token: str, client: str) -> dict:
        data = self.decoder(
            token,
            self.secret,
            algorithms=self.algorithm,
            audience=self._audience,
            issuer=self._issuer,
        )
        if data.get("jti") != client:
            raise self.InvalidToken(token)
        return data

    def get_claims(self, client: str, ttl_hours=24) -> dict:
        return {
            "aud": self._audience,
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=ttl_hours),
            "jti": client,
            "iat": datetime.now(tz=timezone.utc),
            "iss": self._issuer,
            "sub": "client",
        }

    _audience = "localhost"
    _issuer = f"MargayPythonSDK-{socket.gethostname()}"
