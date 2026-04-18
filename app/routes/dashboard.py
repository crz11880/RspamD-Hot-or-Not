from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.classification_service import ClassificationService
from app.services.rspamd_service import RspamdService
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_dashboard_stats(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stats = ClassificationService.get_today_stats(db)
    
    rspamd_status = RspamdService.get_status()
    
    return {
        **stats,
        "rspamd": rspamd_status
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
    return result
