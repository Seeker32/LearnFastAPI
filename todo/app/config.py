import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    app_name: str = "Todo API with SQLModel"
    database_url: str = os.getenv("DATABASE_URL")
    
    # Scrypt password hashing configuration
    # N: CPU/memory cost parameter (must be a power of 2)
    scrypt_n: int = int(os.getenv("SCRYPT_N", str(2 ** 16)))
    
    # r: Block size parameter
    scrypt_r: int = int(os.getenv("SCRYPT_R", "8"))
    
    # p: Parallelization parameter
    scrypt_p: int = int(os.getenv("SCRYPT_P", "1"))
    
    # Salt length in bytes
    salt_length: int = int(os.getenv("SALT_LENGTH", "32"))
    
    # Key (hash) length in bytes
    key_length: int = int(os.getenv("KEY_LENGTH", "32"))


settings = Settings()