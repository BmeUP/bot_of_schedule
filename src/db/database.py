import platform
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.bot.tokens import Apikeys

if 'MANJARO' in platform.release():
    dburi = Apikeys.database_test
else:
    dburi = Apikeys.database_prod

engine = create_engine(dburi, echo=True)
Session = sessionmaker(bind=engine)
s = Session()
