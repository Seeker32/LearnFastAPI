from datetime import datetime, timezone

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class TodoBase(SQLModel):
    title: str = Field(..., min_length=1, max_length=100, description="Title of the todo item")
    description: str | None = Field(default=None, max_length=500, description="Detailed description of the todo item")
    priority: int = Field(default=1, ge=1, le=3, description="Priority of the todo item (1-3)")


class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_delete: bool = Field(default=False, description="Indicates whether the todo is soft deleted")


class TodoCreate(TodoBase):
    """Payload schema for creating a todo item."""


class TodoRead(TodoBase):  
    """Response schema for reading a todo item."""

    id: int
    created_at: datetime
    updated_at: datetime
    is_delete: bool

    model_config = ConfigDict(from_attributes=True)


class TodoUpdate(SQLModel):
    """Payload schema for partially updating a todo item."""

    title: str | None = Field(default=None, min_length=1, max_length=100, description="Updated title of the todo item")
    description: str | None = Field(default=None, max_length=500, description="Updated detailed description of the todo item")
    priority: int | None = Field(default=None, ge=1, le=3, description="Updated priority of the todo item (1-3)")
