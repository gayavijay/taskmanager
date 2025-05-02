# database.py
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from config import DATABASE_URL
import hashlib
import logging

logger = logging.getLogger(__name__)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)  # store hashed

    tasks = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    due_date = Column(Date)
    priority = Column(String)
    category = Column(String)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if session.query(User).filter_by(username=username).first():
        return False
    user = User(username=username, password=hash_password(password))
    session.add(user)
    session.commit()
    logger.info(f"New user registered: {username}")
    return True

def login_user(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and user.password == hash_password(password):
        logger.info(f"User logged in: {username}")
        return user.id
    return None

def add_task(title, due_date, priority, category, user_id):
    try:
        task = Task(title=title, due_date=due_date, priority=priority, category=category, user_id=user_id)
        session.add(task)
        session.commit()
        logger.info(f"Task added: {title}")
    except Exception as e:
        logger.error(f"Failed to add task: {e}")

def get_all_tasks(user_id):
    return session.query(Task).filter_by(user_id=user_id).order_by(Task.due_date).all()

def delete_task(task_id, user_id):
    task = session.query(Task).filter_by(id=task_id, user_id=user_id).first()
    if task:
        session.delete(task)
        session.commit()
        logger.info(f"Task deleted: {task.title}")

def mark_task_complete(task_id, user_id):
    task = session.query(Task).filter_by(id=task_id, user_id=user_id).first()
    if task:
        task.completed = True
        session.commit()
        logger.info(f"Task marked complete: {task.title}")
