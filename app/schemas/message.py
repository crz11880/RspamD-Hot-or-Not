from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MessageResponse(BaseModel):
    id: int
    provider_id: str
    sender: Optional[str] = None
    subject: Optional[str] = None
    received_date: Optional[datetime] = None
    status: str
    score: Optional[str] = None

    class Config:
        from_attributes = True

class MessageDetailResponse(BaseModel):
    id: int
    provider_id: str
    sender: Optional[str] = None
    recipient: Optional[str] = None
    subject: Optional[str] = None
    received_date: Optional[datetime] = None
    status: str
    score: Optional[str] = None
    raw_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
