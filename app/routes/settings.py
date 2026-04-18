from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.settings_service import SettingsService
from app.schemas.settings import SettingsUpdate
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("")
def get_settings(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    settings = SettingsService.get_all_settings(db)
    return settings

@router.get("/{key}")
def get_setting(
    key: str,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    value = SettingsService.get_setting(db, key)
    if value is None:
        return {"key": key, "value": None}
    return {"key": key, "value": value}

@router.put("/{key}")
def update_setting(
    key: str,
    request: SettingsUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    setting = SettingsService.set_setting(db, key, request.value)
    return {"key": setting.key, "value": setting.value}
