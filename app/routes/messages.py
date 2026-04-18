from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.classification_service import ClassificationService
from app.schemas.classification import ClassificationRequest, ClassificationResponse
from app.schemas.message import MessageResponse, MessageDetailResponse
from app.utils.security import get_current_user
from app.config import settings
from app.models.message import Message as MessageModel
from app.models.classification import Classification as ClassificationModel

router = APIRouter(prefix="/api/messages", tags=["messages"])

@router.get("/pending", response_model=list[MessageResponse])
def get_pending_messages(
    limit: int = 50,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    messages = ClassificationService.get_pending_messages(db, limit)
    return messages

@router.get("/next", response_model=MessageDetailResponse)
def get_next_message(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    message = ClassificationService.get_next_pending_message(db)
    if not message:
        raise HTTPException(status_code=404, detail="No pending messages")
    
    detail = {
        "id": message.id,
        "provider_id": message.provider_id,
        "sender": message.sender,
        "recipient": message.recipient,
        "subject": message.subject,
        "received_date": message.received_date,
        "status": message.status,
        "score": message.score,
        "created_at": message.created_at,
        "raw_message": None
    }
    
    if message.raw_message:
        try:
            detail["raw_message"] = message.raw_message.decode('utf-8', errors='ignore')
        except:
            detail["raw_message"] = "(Unable to decode)"
    
    return detail

@router.get("/{message_id}", response_model=MessageDetailResponse)
def get_message_detail(
    message_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    message = db.query(MessageModel).filter(MessageModel.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    detail = {
        "id": message.id,
        "provider_id": message.provider_id,
        "sender": message.sender,
        "recipient": message.recipient,
        "subject": message.subject,
        "received_date": message.received_date,
        "status": message.status,
        "score": message.score,
        "created_at": message.created_at,
        "raw_message": None
    }
    
    if message.raw_message:
        try:
            detail["raw_message"] = message.raw_message.decode('utf-8', errors='ignore')
        except:
            detail["raw_message"] = "(Unable to decode)"
    
    return detail

@router.post("/{message_id}/classify", response_model=ClassificationResponse)
def classify_message(
    message_id: int,
    request: ClassificationRequest,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    classification = ClassificationService.classify_message(
        db=db,
        message_id=message_id,
        user_id=user_id,
        decision=request.decision,
        rspamd_enabled=settings.RSPAMD_ENABLED
    )
    return classification

@router.post("/{message_id}/skip")
def skip_message(
    message_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    message = ClassificationService.skip_message(db, message_id, user_id)
    return {"message_id": message.id, "status": message.status}

@router.get("/history/list")
def get_classification_history(
    limit: int = 100,
    offset: int = 0,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results = ClassificationService.get_classification_history(db, limit, offset)
    
    history = []
    for classification, message in results:
        history.append({
            "id": classification.id,
            "message_id": message.id,
            "sender": message.sender,
            "subject": message.subject,
            "decision": classification.decision,
            "created_at": classification.created_at,
            "rspamd_status": classification.rspamd_submit_status
        })
    
    return history
