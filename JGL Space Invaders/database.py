"""Builds the functionality to work with SQLAlchemy
to keep track of player's Space Invader's score"""

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker


# Define database URI
SPACE_INVADERS_URI = "sqlite:///space_invaders.db"

# Create engines for the database
space_invaders_engine = create_engine(SPACE_INVADERS_URI)

# Create session for the database
SpaceInvadersSession = sessionmaker(bind=space_invaders_engine)
SPACE_INVADERS_SESSION = SpaceInvadersSession()

class Base(DeclarativeBase):
    pass

# Define modules that map to the tables in the existing database
class AlienColors(Base):
    __tablename__ = "alien_colors"
    color_id = Column(Integer, primary_key=True, autoincrement=True)
    color = Column(String)
    
class ScoreValues(Base):
    __tablename__ = "score_values"
    score_id = Column(Integer, primary_key=True, autoincrement=True)
    score_color = Column(Integer, ForeignKey("alien_colors.color_id"))
    value = Column(Integer)