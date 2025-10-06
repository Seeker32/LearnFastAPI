"""CRUD operations for User model."""

import base64
import secrets
from sqlmodel import Session, select
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

from ..config import settings
from ..models import User, UserCreate, UserUpdate


SCRYPT_N = settings.scrypt_n      # CPU/memory cost parameter (default: 131072)
SCRYPT_R = settings.scrypt_r      # Block size parameter (default: 8)
SCRYPT_P = settings.scrypt_p      # Parallelization parameter (default: 1)
SALT_LENGTH = settings.salt_length  # Salt length in bytes (default: 32)
KEY_LENGTH = settings.key_length    # Key length in bytes (default: 32)


def hash_password(password: str) -> str:
    """Hash a plain password using Scrypt from cryptography.
    
    Scrypt is a memory-hard key derivation function that provides
    better resistance against hardware brute-force attacks.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password as string in format: salt$hash
    """
    # Generate a random salt
    salt = secrets.token_bytes(SALT_LENGTH)
    
    # Create Scrypt instance
    kdf = Scrypt(
        salt=salt,
        length=KEY_LENGTH,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        backend=default_backend()
    )
    
    # Derive key from password
    key = kdf.derive(password.encode('utf-8'))
    
    # Encode salt and hash in base64 and combine them
    salt_b64 = base64.b64encode(salt).decode('utf-8')
    hash_b64 = base64.b64encode(key).decode('utf-8')
    
    # Format: salt$hash
    return f"{salt_b64}${hash_b64}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password using Scrypt.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against (format: salt$hash)
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        # Split salt and hash
        salt_b64, hash_b64 = hashed_password.split('$')
        
        # Decode from base64
        salt = base64.b64decode(salt_b64)
        expected_hash = base64.b64decode(hash_b64)
        
        # Create Scrypt instance with the same parameters
        kdf = Scrypt(
            salt=salt,
            length=KEY_LENGTH,
            n=SCRYPT_N,
            r=SCRYPT_R,
            p=SCRYPT_P,
            backend=default_backend()
        )
        
        # Verify the password
        kdf.verify(plain_password.encode('utf-8'), expected_hash)
        return True
    except Exception:
        return False


def create_user(session: Session, user_create: UserCreate) -> User:
    """Create a new user with hashed password.
    
    Args:
        session: Database session
        user_create: UserCreate schema with plain password
        
    Returns:
        Created User instance
    """
    # Extract plain password and hash it
    plain_password = user_create.password.get_secret_value()
    hashed_password = hash_password(plain_password)
    
    # Create user with hashed password
    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_id(session: Session, user_id: int) -> User | None:
    """Get a user by ID."""
    return session.get(User, user_id)


def get_user_by_username(session: Session, username: str) -> User | None:
    """Get a user by username."""
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def get_user_by_email(session: Session, email: str) -> User | None:
    """Get a user by email."""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def update_user(session: Session, user_id: int, user_update: UserUpdate) -> User | None:
    """Update a user.
    
    Args:
        session: Database session
        user_id: ID of the user to update
        user_update: UserUpdate schema with optional fields
        
    Returns:
        Updated User instance or None if not found
    """
    user = session.get(User, user_id)
    if not user:
        return None
    
    # Update fields that are provided
    if user_update.username is not None:
        user.username = user_update.username
    
    if user_update.email is not None:
        user.email = user_update.email
    
    if user_update.password is not None:
        # Hash the new password
        plain_password = user_update.password.get_secret_value()
        user.hashed_password = hash_password(plain_password)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    """Soft delete a user.
    
    Args:
        session: Database session
        user_id: ID of the user to delete
        
    Returns:
        True if deleted, False if not found
    """
    user = session.get(User, user_id)
    if not user:
        return False
    
    user.is_delete = True
    session.add(user)
    session.commit()
    return True


def authenticate_user(session: Session, username: str, password: str) -> User | None:
    """Authenticate a user by username and password.
    
    Args:
        session: Database session
        username: Username
        password: Plain password
        
    Returns:
        User instance if authentication succeeds, None otherwise
    """
    user = get_user_by_username(session, username)
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user

