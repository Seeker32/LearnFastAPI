"""API endpoints for user management."""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session

from ...service import (
    create_user,
    get_user_by_id,
    get_user_by_username,
    get_user_by_email,
    update_user,
    delete_user,
    authenticate_user,
)
from ...dependencies import get_session
from ...models import UserCreate, UserRead, UserUpdate, ApiResponse, success_response, error_response, Token, LoginRequest
from ...security import create_access_token
from ...config import settings

router = APIRouter()


@router.post(
    "",
    response_model=ApiResponse[UserRead],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
def create_user_endpoint(
    user_create: UserCreate,
    session: Session = Depends(get_session),
) -> ApiResponse[UserRead]:
    """Create a new user with the provided information.
    
    The password will be automatically hashed before storing in the database.
    """
    # Check if username already exists
    existing_user = get_user_by_username(session, user_create.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    # Check if email already exists
    existing_email = get_user_by_email(session, str(user_create.email))
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    user = create_user(session, user_create)
    return success_response(data=user, msg="User created successfully")


@router.get(
    "/{user_id}",
    response_model=ApiResponse[UserRead],
    summary="Get a user by ID",
)
def get_user_endpoint(
    user_id: int,
    session: Session = Depends(get_session),
) -> ApiResponse[UserRead]:
    """Retrieve a user by their ID."""
    user = get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    
    if user.is_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} has been deleted",
        )
    
    return success_response(data=user, msg="User retrieved successfully")


@router.patch(
    "/{user_id}",
    response_model=ApiResponse[UserRead],
    summary="Update a user",
)
def update_user_endpoint(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session),
) -> ApiResponse[UserRead]:
    """Update a user's information.
    
    If password is provided, it will be automatically hashed before updating.
    """
    # Check if user exists
    existing_user = get_user_by_id(session, user_id)
    if not existing_user or existing_user.is_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    
    # Check username uniqueness if updating
    if user_update.username and user_update.username != existing_user.username:
        username_taken = get_user_by_username(session, user_update.username)
        if username_taken:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
    
    # Check email uniqueness if updating
    if user_update.email and str(user_update.email) != existing_user.email:
        email_taken = get_user_by_email(session, str(user_update.email))
        if email_taken:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken",
            )
    
    user = update_user(session, user_id, user_update)
    return success_response(data=user, msg="User updated successfully")


@router.delete(
    "/{user_id}",
    response_model=ApiResponse[None],
    summary="Delete a user",
)
def delete_user_endpoint(
    user_id: int,
    session: Session = Depends(get_session),
) -> ApiResponse[None]:
    """Soft delete a user by their ID."""
    success = delete_user(session, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    
    return success_response(data=None, msg="User deleted successfully")


@router.post(
    "/authenticate",
    response_model=ApiResponse[UserRead],
    summary="Authenticate a user",
)
def authenticate_user_endpoint(
    username: str,
    password: str,
    session: Session = Depends(get_session),
) -> ApiResponse[UserRead]:
    """Authenticate a user with username and password."""
    user = authenticate_user(session, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    if user.is_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account has been deleted",
        )
    
    return success_response(data=user, msg="Authentication successful")


@router.post(
    "/login",
    response_model=ApiResponse[Token],
    summary="User login with JWT",
)
def login(
    credentials: LoginRequest,
    session: Session = Depends(get_session),
) -> ApiResponse[Token]:
    user = authenticate_user(session, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    if user.is_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account has been deleted",
        )

    access_token = create_access_token(subject=user.id, extra_claims={"username": user.username})
    expires_in_seconds = settings.access_token_expires_minutes * 60
    token = Token(access_token=access_token, token_type="bearer", expires_in=expires_in_seconds)
    return success_response(data=token, msg="Login successful")

