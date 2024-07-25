

from flask import Flask
from flask_login import UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Time as sqla_time

app = Flask(__name__)

# Create Database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks_todo.db"
migrate = Migrate(app, db)

# Configure Tables
class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    pref_starting_day: Mapped[int] = mapped_column(Integer, nullable=True)
    tasks = relationship("Tasks", backref="user")
    
class Tasks(db.Model):
    __tablename__ = "tasks"
    task_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    task_name: Mapped[str] = mapped_column(String(250), nullable=False)
    task_date: Mapped[str] = mapped_column(String(250), nullable=False)
    task_time: Mapped[sqla_time] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    priority_level: Mapped[int] = mapped_column(Integer, nullable=False)
    task_color: Mapped[str] = mapped_column(String(10), nullable=False)
    
    