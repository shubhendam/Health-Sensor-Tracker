import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User

# Get the directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the database file
DB_PATH = os.path.join(BASE_DIR, "test.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to add a new user
def create_user(db, username, password_hash, name, age, gender, weight, location, daily_step_goal):
    user = User(
        username=username,
        password_hash=password_hash,
        name=name,
        age=age,
        gender=gender,
        weight=weight,
        location=location,
        daily_step_goal=daily_step_goal
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Function to get a user by username
def get_user_by_username(db, username):
    return db.query(User).filter(User.username == username).first()

# Function to update user steps
def update_user_steps(db, user_id, steps):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.current_steps = steps
        db.commit()
        db.refresh(user)
    return user

# Function to update user location
def update_user_location(db, user_id, location):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.location = location
        db.commit()
        db.refresh(user)
    return user
