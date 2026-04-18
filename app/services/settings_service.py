from typing import Optional
from sqlalchemy.orm import Session
from app.models.settings import Settings as SettingsModel

class SettingsService:
    
    @staticmethod
    def get_setting(db: Session, key: str, default: str = None) -> Optional[str]:
        setting = db.query(SettingsModel).filter(SettingsModel.key == key).first()
        return setting.value if setting else default
    
    @staticmethod
    def set_setting(db: Session, key: str, value: str) -> SettingsModel:
        setting = db.query(SettingsModel).filter(SettingsModel.key == key).first()
        if setting:
            setting.value = value
        else:
            setting = SettingsModel(key=key, value=value)
            db.add(setting)
        db.commit()
        db.refresh(setting)
        return setting
    
    @staticmethod
    def get_all_settings(db: Session) -> dict:
        settings = db.query(SettingsModel).all()
        return {s.key: s.value for s in settings}
