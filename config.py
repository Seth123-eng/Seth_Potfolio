
import os

from dotenv import load_dotenv

load_dotenv()    

class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')

    TEMPLATES_AUTO_RELOAD = True

     
    #SERVER_NAME = ""
    PREFERRED_URL_SCHEME = "https"


    MAX_CONTENT_LENGTH = 5 * 1024 * 1024


    CKEDITOR_EXTRA_CONFIG = {
    'ignoreEmptyParagraph': True,
    'removePlugins': 'notification',
    }



    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    
    # Allowed HTML tags
    BLEACH_ALLOWED_TAGS = [
    "em", "i", "li", "ol", "strong", "tr", "td", "th", "thead", "ul", "tbody", "table", "figure",
    "p", "span", "s", "strike", "pre", "h1", "h2","h3","h4","h5","h6","b", "blockquote", "hr"
]

    # Allowed HTML attributes
    BLEACH_ALLOWED_ATTRIBUTES = {
    "abbr": ["title"],
    "acronym": ["title"],
}

    # Allowed URL protocols
    BLEACH_ALLOWED_PROTOCOLS = ["http", "https", "mailto"]

    BLEACH_STRIP_TAGS = False

    # Strip HTML comments
    BLEACH_STRIP_COMMENTS = True