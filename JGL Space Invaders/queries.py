"""Responsible for space_invaders.db querying"""

from database import SPACE_INVADERS_SESSION, AlienColors, ScoreValues

# Create session for database querying
si_session = SPACE_INVADERS_SESSION

def jgl_find_color_id(color_name):
    """Returns the color_id for a particular alien's color"""
    
    color_id = si_session.query(
        AlienColors
    ).filter_by(color = color_name).one()
    
    return color_id.color_id

def jgl_find_score_value(color_id):
    """Gets the score value of the alien"""
    
    score = si_session.query(
        ScoreValues
    ).filter_by(score_color = color_id).one()
    
    return score.value
    
    