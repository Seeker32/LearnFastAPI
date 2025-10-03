"""Application wide dependencies."""

from collections.abc import Generator

from sqlmodel import Session

from .database import get_session


def get_db_session() -> Generator[Session, None, None]:
    """Provide a database session for request scope."""

    yield from get_session()

