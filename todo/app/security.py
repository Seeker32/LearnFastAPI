from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from .config import settings


def create_access_token(subject: str | int, extra_claims: dict[str, Any] | None = None) -> str:
    """Create a signed JWT access token.

    Args:
        subject: Unique identifier for the token subject (e.g., user id or username)
        expires_delta_minutes: Minutes until expiration; defaults to settings.access_token_expires_minutes
        extra_claims: Optional additional JWT claims to embed

    Returns:
        Encoded JWT string
    """
    expire_minutes = settings.access_token_expires_minutes
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minutes)

    to_encode: dict[str, Any] = {"sub": str(subject), "iat": int(now.timestamp()), "exp": int(expire.timestamp())}
    if extra_claims:
        to_encode.update(extra_claims)

    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


