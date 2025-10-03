"""Todo API endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from ...crud import (
    create_todo,
    get_todo,
    list_todos,
    permanently_delete_todo,
    soft_delete_todo,
    update_todo,
)
from ...dependencies import get_db_session
from ...models import TodoCreate, TodoRead, TodoUpdate, success_response, error_response


router = APIRouter()


@router.get("/")
def read_todos(
    *,
    include_deleted: bool = Query(False, description="Whether to include soft deleted todos"),
    session: Session = Depends(get_db_session),
) -> dict[str, Any]:
    todos = list_todos(session, include_deleted=include_deleted)
    todo_list = [TodoRead.model_validate(todo) for todo in todos]
    return success_response(data=todo_list, msg="Todos retrieved successfully")


@router.get("/{todo_id}")
def read_todo(todo_id: int, session: Session = Depends(get_db_session)) -> dict[str, Any]:
    todo = get_todo(session, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(msg="Todo not found", code=404)
        )
    return success_response(data=TodoRead.model_validate(todo), msg="Todo retrieved successfully")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_todo_item(
    payload: TodoCreate,
    session: Session = Depends(get_db_session),
) -> dict[str, Any]:
    todo = create_todo(session, payload)
    return success_response(data=TodoRead.model_validate(todo), msg="Todo created successfully", code=201)


@router.patch("/{todo_id}")
def update_todo_item(
    todo_id: int,
    payload: TodoUpdate,
    session: Session = Depends(get_db_session),
) -> dict[str, Any]:
    todo = update_todo(session, todo_id, payload)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(msg="Todo not found", code=404)
        )
    return success_response(data=TodoRead.model_validate(todo), msg="Todo updated successfully")


@router.delete("/{todo_id}")
def delete_todo_item(todo_id: int, session: Session = Depends(get_db_session)) -> dict[str, Any]:
    deleted = soft_delete_todo(session, todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(msg="Todo not found or already deleted", code=404)
        )
    return success_response(msg="Todo deleted successfully")


@router.delete("/{todo_id}/permanent")
def delete_todo_permanently(todo_id: int, session: Session = Depends(get_db_session)) -> dict[str, Any]:
    deleted = permanently_delete_todo(session, todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(msg="Todo not found", code=404)
        )
    return success_response(msg="Todo permanently deleted successfully")

