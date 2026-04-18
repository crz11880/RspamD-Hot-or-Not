from sqlalchemy import Column, Integer, String, DateTime, Text, LargeBinary
from sqlalchemy.sql import func
from app.db import Base

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(String(255), nullable=False)
    provider_type = Column(String(50), nullable=False)
    sender = Column(String(255), index=True)
    recipient = Column(String(255))
    subject = Column(String(500))
    received_date = Column(DateTime(timezone=True))
    raw_message = Column(LargeBinary)
    message_hash = Column(String(64), unique=True, index=True)
    status = Column(String(20), default="pending", index=True)
    score = Column(String(50))
    source_path = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
