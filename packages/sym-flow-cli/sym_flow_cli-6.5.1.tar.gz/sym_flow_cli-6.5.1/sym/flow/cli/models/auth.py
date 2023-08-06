from pydantic import BaseModel

from sym.flow.cli.errors import InvalidTokenError


class AuthToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


def parse_auth_token(json_response: dict) -> AuthToken:
    try:
        return AuthToken(
            access_token=json_response["access_token"],
            token_type=json_response["token_type"],
            expires_in=json_response["expires_in"],
        )
    except KeyError:
        raise InvalidTokenError(str(json_response))
