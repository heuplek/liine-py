from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import configparser 

config = configparser.RawConfigParser()
config.read('config.properties')
db_user = config.get('DataBaseSection', 'dbuser')
db_password = config.get('DataBaseSection', 'dbpassword')
db_name = config.get('DataBaseSection', 'dbname')
SQLALCHEMY_DATABASE_URL = f'postgresql://{db_user}:{db_password}@localhost/{db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()