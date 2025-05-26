from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
'''
create connection to sqlite database
'''
 
db_url = 'sqlite:///mnts/coffeeproto_v1.db'
engine = create_engine(db_url)
Base = declarative_base()