from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog

class AuditLogService:
    
    @staticmethod
    def log_action(
        db: Session,
        user_id: int,
        action: str,
        resource_type: str = None,
        resource_id: int = None,
        details: str = None
    ) -> AuditLog:
        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry
    
    @staticmethod
    def get_logs(db: Session, limit: int = 100, offset: int = 0) -> list[AuditLog]:
        return db.query(AuditLog).order_by(
            AuditLog.created_at.desc()
        ).limit(limit).offset(offset).all()
