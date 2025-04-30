from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)  # Male/Female/Other
    weight = Column(Float, nullable=False)
    location = Column(String, nullable=True)
    daily_step_goal = Column(Integer, nullable=False)
    current_steps = Column(Integer, default=0)
    last_updated = Column(String, nullable=True)  # To store last update date if needed later
