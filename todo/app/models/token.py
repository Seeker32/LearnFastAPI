from sqlmodel import SQLModel, Field

class LoginRequest(SQLModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=128)


class Token(SQLModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type, typically 'bearer'")
    expires_in: int = Field(default=3600, description="Token expiration time in seconds")


