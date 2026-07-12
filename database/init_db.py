from database.database import Base, engine
# Import all models here so SQLAlchemy knows about them
from database.models import Weather


def init_db():
    Base.metadata.create_all(bind=engine)
