from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not configured.")
engine = create_engine(DATABASE_URL, pool_size=5,max_overflow=10, pool_timeout=30, pool_pre_ping=True)

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

   

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="New Chat")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False
    )
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )

Base.metadata.create_all(bind=engine)

