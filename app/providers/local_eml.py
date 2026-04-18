import os
import email
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Union
from app.providers.base import MessageProvider

class LocalEmlProvider(MessageProvider):
    
    def __init__(self, email_dir: str):
        self.email_dir = Path(email_dir)
        self.processed_dir = self.email_dir / "processed"
        self.spam_dir = self.processed_dir / "spam"
        self.ham_dir = self.processed_dir / "ham"
        self.skipped_dir = self.processed_dir / "skipped"
        
        self.email_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.spam_dir.mkdir(parents=True, exist_ok=True)
        self.ham_dir.mkdir(parents=True, exist_ok=True)
        self.skipped_dir.mkdir(parents=True, exist_ok=True)
    
    def list_pending_messages(self) -> List[Dict]:
        messages = []
        for eml_file in sorted(self.email_dir.glob("*.eml")):
            msg_dict = self._parse_eml_file(eml_file)
            if msg_dict:
                messages.append(msg_dict)
        return messages
    
    def get_message(self, provider_id: str) -> Optional[Dict]:
        eml_path = self.email_dir / provider_id
        if eml_path.exists() and eml_path.suffix == ".eml":
            return self._parse_eml_file(eml_path)
        return None
    
    def get_raw_message(self, provider_id: str) -> Optional[bytes]:
        eml_path = self.email_dir / provider_id
        if eml_path.exists() and eml_path.suffix == ".eml":
            return eml_path.read_bytes()
        return None
    
    def mark_processed(self, provider_id: str, status: str):
        eml_path = self.email_dir / provider_id
        if not eml_path.exists():
            return
        
        if status == "spam":
            target_dir = self.spam_dir
        elif status == "ham":
            target_dir = self.ham_dir
        else:
            target_dir = self.skipped_dir
        
        target_path = target_dir / provider_id
        eml_path.rename(target_path)
    
    def skip_message(self, provider_id: str):
        self.mark_processed(provider_id, "skipped")
    
    def _parse_eml_file(self, eml_path: Path) -> Optional[Dict]:
        try:
            with open(eml_path, "rb") as f:
                raw_data = f.read()
            
            msg = email.message_from_bytes(raw_data)
            
            sender = msg.get("From", "Unknown")
            recipient = msg.get("To", "Unknown")
            subject = msg.get("Subject", "(No Subject)")
            date_str = msg.get("Date", "")
            
            received_date = None
            if date_str:
                try:
                    from email.utils import parsedate_to_datetime
                    received_date = parsedate_to_datetime(date_str)
                except:
                    pass
            
            message_hash = hashlib.sha256(raw_data).hexdigest()
            
            body = self._extract_text_body(msg)
            
            return {
                "provider_id": eml_path.name,
                "provider_type": "local_eml",
                "sender": sender,
                "recipient": recipient,
                "subject": subject,
                "received_date": received_date,
                "raw_message": raw_data,
                "message_hash": message_hash,
                "source_path": str(eml_path),
                "body_preview": body[:500] if body else "(No text body)"
            }
        except Exception as e:
            print(f"Error parsing {eml_path}: {e}")
            return None
    
    def _extract_text_body(self, msg) -> str:
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        pass
        else:
            if msg.get_content_type() == "text/plain":
                try:
                    body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                except:
                    body = msg.get_payload()
        
        return body.strip()
