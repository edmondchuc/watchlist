try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from os import environ

# Flask
SECRET_KEY = environ.get('SECRET_KEY', 'a-very-bad-secret-key-please-use-something-else')

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///../watchlist.db')

# TMDb
TMDB_API_KEY = environ.get('TMDB_API_KEY')
TMDB_BASE_IMAGE_URL = environ.get('TMDB_BASE_IMAGE_URL', 'http://image.tmdb.org/t/p/w200')
