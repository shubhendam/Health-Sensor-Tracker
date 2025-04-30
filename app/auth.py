from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import get_db, create_user, get_user_by_username
from models import User

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against a plain password."""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str) -> User:
    """Authenticate a user by checking the username and password."""
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def register_user(db: Session, username: str, password: str, name: str, age: int, gender: str, weight: float, location: str, daily_step_goal: int) -> User:
    """Register a new user."""
    hashed_password = hash_password(password)
    return create_user(db, username, hashed_password, name, age, gender, weight, location, daily_step_goal)
