from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.db import get_db
from app.services.classification_service import ClassificationService
from app.services.rspamd_service import RspamdService
from app.services.settings_service import SettingsService
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_dashboard_stats(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stats = ClassificationService.get_today_stats(db)
    
    rspamd_status = RspamdService.get_status()
    last_sync_new = SettingsService.get_setting(db, "last_sync_new_messages", "0")
    last_sync_duplicates = SettingsService.get_setting(db, "last_sync_duplicates", "0")
    last_sync_total = SettingsService.get_setting(db, "last_sync_total", "0")
    last_sync_at = SettingsService.get_setting(db, "last_sync_at", "")
    
    return {
        **stats,
        "rspamd": rspamd_status,
        "last_sync": {
            "new_messages": int(last_sync_new or 0),
            "duplicates": int(last_sync_duplicates or 0),
            "total": int(last_sync_total or 0),
            "at": last_sync_at
        }
    }

@router.get("/recent-activities")
def get_recent_activities(
    limit: int = 20,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.services.audit_log_service import AuditLogService
    logs = AuditLogService.get_logs(db, limit)
    
    activities = []
    for log in logs:
        activities.append({
            "id": log.id,
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "created_at": log.created_at
        })
    
    return activities

@router.post("/sync-messages")
def sync_messages(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.utils.message_sync import MessageSyncService
    result = MessageSyncService.sync_messages_from_provider(db)

    SettingsService.set_setting(db, "last_sync_new_messages", str(result.get("new_messages", 0)))
    SettingsService.set_setting(db, "last_sync_duplicates", str(result.get("duplicates_skipped", 0)))
    SettingsService.set_setting(db, "last_sync_total", str(result.get("total", 0)))
    SettingsService.set_setting(db, "last_sync_at", datetime.now(timezone.utc).isoformat())

    return result
