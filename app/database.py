from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from utils import DB_URL

engine = create_engine("mysql+mysqlconnector://root@127.0.0.1:3306/dolt", echo=True)

Base = declarative_base()

