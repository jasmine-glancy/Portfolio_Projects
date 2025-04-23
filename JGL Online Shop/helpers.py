from datetime import datetime
import os

def current_year():
    """Returns the current year"""
    
    # Convert current date to a string
    jgl_date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    # Grab only the year
    jgl_current_year = jgl_date_str[:4]
    
    return jgl_current_year

def social_links():
    """Returns the social media links"""
    
    github = os.environ.get("github")
    linkedin = os.environ.get("linkedin")
    discord = os.environ.get("discord")
    fiverr = os.environ.get("fiverr")
    email = os.environ.get("email")
    youtube = os.environ.get("youtube")
    patreon = os.environ.get("patreon")
    
    socials = {
        "github_link": github,
        "linkedin_link": linkedin,
        "discord_link": discord,
        "fiverr_link": fiverr,
        "email_address": email,
        "youtube_link": youtube,
        "patreon": patreon
        }
    
    return socials
