from pydantic import BaseModel, Field
from datetime import datetime

class ClassificationRequest(BaseModel):
    decision: str = Field(..., pattern="^(spam|ham|skipped)$")

class ClassificationResponse(BaseModel):
    id: int
    message_id: int
    decision: str
    rspamd_submit_status: str
    created_at: datetime

    class Config:
        from_attributes = True
