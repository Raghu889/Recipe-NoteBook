from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@host.docker.internal:3306/recipes_db"

engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()
