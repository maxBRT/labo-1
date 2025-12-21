from location.database.database_manager import DatabaseManager
from location.database.database import Base, engine
from location.database.models import *


def main():
    # Initialize the database
    Base.metadata.create_all(bind=engine)
    db = DatabaseManager()
    db.seed()


if __name__ == "__main__":
    main()
