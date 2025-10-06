"""CRUD helper functions for todos."""

from datetime import datetime, timezone
from typing import Iterable

from sqlmodel import Session, select

from ..models import Todo, TodoCreate, TodoUpdate


def create_todo(session: Session, payload: TodoCreate) -> Todo:
    """Create a todo record."""

    todo = Todo(**payload.model_dump())
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def list_todos(session: Session, *, include_deleted: bool = False) -> list[Todo]:
    """Return all todos."""

    statement = select(Todo)
    if not include_deleted:
        statement = statement.where(Todo.is_delete.is_(False))
    todos = session.exec(statement).all()
    return todos


def get_todo(session: Session, todo_id: int, *, include_deleted: bool = False) -> Todo | None:
    """Return a todo by its ID."""

    todo = session.get(Todo, todo_id)
    if todo and not include_deleted and todo.is_delete:
        return None
    return todo


def update_todo(session: Session, todo_id: int, payload: TodoUpdate) -> Todo | None:
    """Update a todo record."""

    todo = session.get(Todo, todo_id)
    if not todo:
        return None

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(todo, field, value)
    todo.updated_at = datetime.now(timezone.utc)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def soft_delete_todo(session: Session, todo_id: int) -> bool:
    """Soft delete a todo by marking it deleted."""

    todo = session.get(Todo, todo_id)
    if not todo or todo.is_delete:
        return False

    todo.is_delete = True
    todo.updated_at = datetime.now(timezone.utc)
    session.add(todo)
    session.commit()
    return True


def permanently_delete_todo(session: Session, todo_id: int) -> bool:
    """Hard delete a todo."""

    todo = session.get(Todo, todo_id)
    if not todo:
        return False

    session.delete(todo)
    session.commit()
    return True

