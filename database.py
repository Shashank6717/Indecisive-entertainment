from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./movies.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class MovieDB(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    director = Column(String, nullable=False)
    cast = Column(String, nullable=False)
    genres = Column(String, nullable=False)
    language = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    synopsis = Column(Text, nullable=False)
    streaming_platforms = Column(String, nullable=False)
    poster_url = Column(String, nullable=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
