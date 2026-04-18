from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db import Base

class Classification(Base):
    __tablename__ = "classifications"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    decision = Column(String(20), index=True)
    rspamd_submit_status = Column(String(20), default="pending")
    rspamd_response = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
