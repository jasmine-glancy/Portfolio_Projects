"""Imports staff_initials.db and allows queries"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Define database URI
STAFF_INITIALS_URI = "sqlite:///staff_initials.db"

# Create engines for the database
staff_initials_engine = create_engine(STAFF_INITIALS_URI)

# Create session for the database
StaffInitialsSession = sessionmaker(bind=staff_initials_engine)
STAFF_INITIALS_SESSION = StaffInitialsSession()

class Base(DeclarativeBase):
    pass

# Define modules that map to the tables in the existing database
class Doctors(Base):
    __tablename__ = "Doctors"
    dr_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    cs_initials = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    notes = Column(String)
 
class Staff(Base):   
    __tablename__ = "Staff"
    staff_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    cs_initials = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    notes = Column(String)