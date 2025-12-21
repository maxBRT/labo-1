from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./my_app.db"

# Create the Engine
engine = create_engine(DATABASE_URL, echo=True)

# Create the SessionLocal class
SessionLocal = sessionmaker(bind=engine)

# Create the Base class
Base = declarative_base()
