from sqlmodel import create_engine

from config.psql import POSTGRES_DB_URL

engine = create_engine(POSTGRES_DB_URL, echo=False)
