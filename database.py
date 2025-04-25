from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    due_date = Column(Date)
    priority = Column(String)
    category = Column(String)
    completed = Column(Boolean, default=False)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_task(title, due_date, priority, category):
    task = Task(title=title, due_date=due_date, priority=priority, category=category)
    session.add(task)
    session.commit()

def get_all_tasks():
    return session.query(Task).order_by(Task.due_date).all()

def delete_task(task_id):
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()

def mark_task_complete(task_id):
    task = session.query(Task).get(task_id)
    if task:
        task.completed = True
        session.commit()