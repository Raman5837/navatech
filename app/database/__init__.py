from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from env import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as exception:
        db.rollback()
        print(f"[DB Exception]: {exception}")
    finally:
        db.close()


class DBManager:
    """ """

    def create(self, name: str) -> Dict:
        """
        Creates New Dynamic DB
        """

        engine = create_engine(f"sqlite:///./{name}.db", echo=True)
        Base.metadata.create_all(bind=engine)
        return {"name": name, "url": f"./{name}.db"}
