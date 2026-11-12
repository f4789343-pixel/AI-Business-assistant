from sqlalchemy import declarative_base, create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite://./business.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thred":False}, pool_size=5,max_overflow=10, pool_timeout=30, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()
def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()

class Customers(Base):
  __tablename__ = "customers"
  customer_id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False, unique=False)
  email = Column(String, nullable=False, unique=True)

Base.metadata.create_all(bind=engine)

