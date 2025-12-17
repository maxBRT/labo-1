from database_manager import DatabaseManager
from database import Base, engine
from models import *


def main():
    # Initialize the database
    Base.metadata.create_all(bind=engine)
    db = DatabaseManager()
    db.seed()


if __name__ == "__main__":
    main()
