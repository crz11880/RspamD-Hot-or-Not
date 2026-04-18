from sqlalchemy.orm import Session
from app.models.message import Message as MessageModel
from app.providers.factory import get_provider
from app.config import EMAILS_DIR
import hashlib

class MessageSyncService:
    
    @staticmethod
    def sync_messages_from_provider(db: Session) -> dict:
        provider = get_provider()
        pending_messages = provider.list_pending_messages()
        
        new_count = 0
        duplicate_count = 0
        
        for msg_data in pending_messages:
            msg_hash = msg_data.get("message_hash")
            existing = db.query(MessageModel).filter(
                MessageModel.message_hash == msg_hash
            ).first()
            
            if existing:
                duplicate_count += 1
                continue
            
            message = MessageModel(
                provider_id=msg_data["provider_id"],
                provider_type=msg_data["provider_type"],
                sender=msg_data.get("sender"),
                recipient=msg_data.get("recipient"),
                subject=msg_data.get("subject"),
                received_date=msg_data.get("received_date"),
                raw_message=msg_data.get("raw_message"),
                message_hash=msg_hash,
                status="pending",
                source_path=msg_data.get("source_path")
            )
            db.add(message)
            new_count += 1
        
        db.commit()
        
        return {
            "new_messages": new_count,
            "duplicates_skipped": duplicate_count,
            "total": len(pending_messages)
        }
