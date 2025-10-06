from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict, EmailStr, SecretStr


class UserBase(SQLModel):
    """Base user schema with common fields (excluding password)."""
    username: str = Field(..., min_length=1, max_length=20, description="Username of the user")
    email: EmailStr = Field(..., description="Email of the user")


class User(UserBase, table=True):
    """Database model for user with hashed password."""
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(..., max_length=255, description="Hashed password of the user")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_delete: bool = Field(default=False, description="Indicates whether the user is soft deleted")


class UserCreate(UserBase):
    """Request schema for creating a user (with plain password)."""
    password: SecretStr = Field(..., min_length=8, max_length=20, description="Password of the user")


class UserUpdate(SQLModel):
    """Request schema for updating a user (all fields optional)."""
    username: str | None = Field(default=None, min_length=1, max_length=20, description="Updated username")
    email: EmailStr | None = Field(default=None, description="Updated email")
    password: SecretStr | None = Field(default=None, min_length=8, max_length=20, description="Updated password")


class UserRead(UserBase):
    """Response schema for reading a user (without password)."""
    id: int
    created_at: datetime
    updated_at: datetime
    is_delete: bool

    model_config = ConfigDict(from_attributes=True)
