from pydantic import BaseModel, Field
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool
    must_change_credentials: bool
    created_at: datetime

    class Config:
        from_attributes = True


class InitialCredentialsUpdate(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_username: str = Field(..., min_length=3, max_length=50)
    new_password: str = Field(..., min_length=8)


class ChangeCredentials(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_username: str = Field(..., min_length=3, max_length=50)
    new_password: str = Field(..., min_length=8)
