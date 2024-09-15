"""Responsible for space_invaders.db querying"""

from database import SPACE_INVADERS_SESSION, AlienColors, HighScores, ScoreValues
from sqlalchemy import desc

# Create session for database querying
si_session = SPACE_INVADERS_SESSION

def jgl_find_color_id(color_name) -> int:
    """Returns the color_id for a particular alien's color"""
    
    color_id = si_session.query(
        AlienColors
    ).filter_by(color = color_name).one()
    
    return color_id.color_id

def jgl_find_score_value(color_id) -> int:
    """Gets the score value of the alien"""
    
    score = si_session.query(
        ScoreValues
    ).filter_by(score_color = color_id).one()
    
    return score.value

def jgl_find_top_scores() -> list:
    """Finds the top 10 scores"""
    
    top_scores = si_session.query(
        HighScores
    ).order_by(desc(HighScores.score)).limit(10).all()
     
    return top_scores

    
    