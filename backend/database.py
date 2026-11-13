from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./business.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread":False}, pool_size=5,max_overflow=10, pool_timeout=30, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()
def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()

class Customer(Base):
  __tablename__ = "customers"
  customer_id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False, unique=False)
  email = Column(String, nullable=False, unique=True)

class Order(Base):
   __tablename__ = "orders"
   order_id = Column(Integer, primary_key=True)
   customer_id = Column(Integer, ForeignKey("customers.customer_id"))
   status = Column(String, nullable=False)
   amount = Column(Float, nullable=False)

class Lead(Base):
   __tablename__ = "leads"
   lead_id = Column(Integer, primary_key=True)
   name = Column(String,nullable=False)
   email = Column(String, nullable=False, unique=True)
   source = Column(String)

Base.metadata.create_all(bind=engine)

   

