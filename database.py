from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./my_app.db"

# 2. Create the Engine
engine = create_engine(DATABASE_URL, echo=True)

# 3. Create the SessionLocal class
SessionLocal = sessionmaker(bind=engine)

# 4. Create the Base class
Base = declarative_base()
