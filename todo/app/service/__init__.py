"""CRUD operations for application models."""

from .todo import (
    create_todo,
    get_todo,
    list_todos,
    permanently_delete_todo,
    soft_delete_todo,
    update_todo,
)
from .user import (
    authenticate_user,
    create_user,
    delete_user,
    get_user_by_email,
    get_user_by_id,
    get_user_by_username,
    hash_password,
    update_user,
    verify_password,
)

__all__ = [
    "create_todo",
    "get_todo",
    "list_todos",
    "permanently_delete_todo",
    "soft_delete_todo",
    "update_todo",
    "authenticate_user",
    "create_user",
    "delete_user",
    "get_user_by_email",
    "get_user_by_id",
    "get_user_by_username",
    "hash_password",
    "update_user",
    "verify_password",
]

