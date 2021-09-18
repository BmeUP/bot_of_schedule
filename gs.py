from src.gsp.gspmain import get_sheet
from src.db.database import engine
from src.db.models.base import Base

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    get_sheet()