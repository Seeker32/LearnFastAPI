from typing import Any

from sqlalchemy.engine import make_url
from sqlmodel import SQLModel, Session, create_engine

from .config import settings


def _build_connect_args(database_url: str) -> dict[str, Any]:
    """Return engine connect arguments based on backend."""

    url = make_url(database_url)
    if url.get_backend_name() == "sqlite":
        return {"check_same_thread": False}
    return {}


# 创建数据库引擎
engine = create_engine(
    settings.database_url,
    echo=True,
    connect_args=_build_connect_args(settings.database_url),
)

def create_db_and_tables():
    """创建数据库和表"""
    SQLModel.metadata.create_all(engine)
    
def get_session():
    """获取数据库会话"""
    with Session(engine) as session:
        yield session