from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.message import Message as MessageModel
from app.models.classification import Classification as ClassificationModel
from app.services.rspamd_service import RspamdService
from app.services.audit_log_service import AuditLogService
from datetime import datetime, timedelta

class ClassificationService:
    
    @staticmethod
    def classify_message(
        db: Session,
        message_id: int,
        user_id: int,
        decision: str,
        rspamd_enabled: bool = False
    ) -> ClassificationModel:
        message = db.query(MessageModel).filter(MessageModel.id == message_id).first()
        if not message:
            raise ValueError("Message not found")
        
        if message.status != "pending":
            raise ValueError(f"Message already classified: {message.status}")
        
        classification = ClassificationModel(
            message_id=message_id,
            user_id=user_id,
            decision=decision,
            rspamd_submit_status="pending" if rspamd_enabled else "skipped"
        )
        
        message.status = "classified"
        
        if rspamd_enabled and message.raw_message:
            try:
                response = RspamdService.learn_message(message.raw_message, decision)
                classification.rspamd_submit_status = "success"
                classification.rspamd_response = str(response)
            except Exception as e:
                classification.rspamd_submit_status = "failed"
                classification.rspamd_response = str(e)
        
        db.add(classification)
        db.commit()
        db.refresh(classification)
        
        AuditLogService.log_action(
            db=db,
            user_id=user_id,
            action="classify_message",
            resource_type="message",
            resource_id=message_id,
            details=f"Decision: {decision}, Rspamd: {classification.rspamd_submit_status}"
        )
        
        return classification
    
    @staticmethod
    def skip_message(db: Session, message_id: int, user_id: int) -> MessageModel:
        message = db.query(MessageModel).filter(MessageModel.id == message_id).first()
        if not message:
            raise ValueError("Message not found")
        
        message.status = "skipped"
        db.commit()
        
        AuditLogService.log_action(
            db=db,
            user_id=user_id,
            action="skip_message",
            resource_type="message",
            resource_id=message_id
        )
        
        return message
    
    @staticmethod
    def get_pending_messages(db: Session, limit: int = 50) -> List[MessageModel]:
        return db.query(MessageModel).filter(
            MessageModel.status == "pending"
        ).order_by(MessageModel.received_date.desc()).limit(limit).all()
    
    @staticmethod
    def get_next_pending_message(db: Session) -> Optional[MessageModel]:
        return db.query(MessageModel).filter(
            MessageModel.status == "pending"
        ).order_by(MessageModel.received_date.desc()).first()
    
    @staticmethod
    def get_classification_history(db: Session, limit: int = 100, offset: int = 0) -> list:
        return db.query(
            ClassificationModel,
            MessageModel
        ).join(MessageModel).order_by(
            ClassificationModel.created_at.desc()
        ).limit(limit).offset(offset).all()
    
    @staticmethod
    def get_today_stats(db: Session) -> dict:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        spam_count = db.query(func.count(ClassificationModel.id)).filter(
            ClassificationModel.decision == "spam",
            ClassificationModel.created_at >= today_start
        ).scalar() or 0
        
        ham_count = db.query(func.count(ClassificationModel.id)).filter(
            ClassificationModel.decision == "ham",
            ClassificationModel.created_at >= today_start
        ).scalar() or 0
        
        pending_count = db.query(func.count(MessageModel.id)).filter(
            MessageModel.status == "pending"
        ).scalar() or 0
        
        total_processed = db.query(func.count(ClassificationModel.id)).scalar() or 0
        
        return {
            "spam_today": spam_count,
            "ham_today": ham_count,
            "pending_count": pending_count,
            "total_processed": total_processed
        }
