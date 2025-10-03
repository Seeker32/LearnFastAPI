import os
from typing import Optional

class Settings:
    app_name: str = "Todo API with SQLModel"
    database_url: str = os.getenv("DATABASE_URL")
    
settings = Settings()