from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db import get_db
from app.utils.security import get_current_user
from app.utils.message_sync import MessageSyncService
from app.config import EMAILS_DIR

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.post("/init-database")
def init_database(user_id: int = Depends(get_current_user)):
    from app.db import init_db
    init_db()
    return {"message": "Database initialized"}

@router.post("/sync-emails")
def sync_emails(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = MessageSyncService.sync_messages_from_provider(db)
    return result

@router.post("/upload-email")
def upload_email(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user)
):
    if not file.filename.endswith(".eml"):
        return {"error": "Only .eml files allowed"}
    
    save_path = EMAILS_DIR / file.filename
    
    import aiofiles
    import asyncio
    
    async def save():
        async with aiofiles.open(save_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
    
    asyncio.run(save())
    
    return {"message": "Email uploaded", "filename": file.filename}
