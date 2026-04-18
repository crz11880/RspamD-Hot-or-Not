from functools import wraps
from typing import Dict
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
from app.db import get_db
import json
from datetime import datetime, timedelta
import secrets

security = HTTPBearer()

# Simple in-memory session store for demo purposes
_sessions: Dict[str, Dict] = {}

def create_session_token(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    _sessions[token] = {
        "user_id": user_id,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(days=7)
    }
    return token

def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    session = _sessions.get(token)
    
    if not session or session["expires_at"] < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    return session["user_id"]

def logout_session(token: str):
    if token in _sessions:
        del _sessions[token]

def get_session_token_from_request(credentials: HTTPAuthCredentials = Depends(security)) -> str:
    return credentials.credentials
