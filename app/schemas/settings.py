from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SettingsResponse(BaseModel):
    key: str
    value: str

class SettingsUpdate(BaseModel):
    value: str

class DashboardStats(BaseModel):
    pending_count: int
    spam_today: int
    ham_today: int
    total_processed: int
    last_activities: list
