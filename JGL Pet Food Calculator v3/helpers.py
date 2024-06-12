"""Contains additional checks and decorators (i.e. is user logged in, login decorator)"""

from flask import session

def clear_variable_list():
    """Clear all pet session variables, code reformatting suggested by CoPilot"""
    
    for variable in list(session.keys()):
        if variable != "user_id":
            session.pop(variable, None)
   

