from typing import Union, Dict
from app.config import settings
from app.utils.rspamd_client import RspamdHTTPClient, RspamdRspamdcClient
import subprocess
import json

class RspamdService:
    _client = None
    
    @classmethod
    def _get_client(cls):
        if cls._client is None:
            if settings.LEARN_COMMAND_TYPE == "http":
                cls._client = RspamdHTTPClient(
                    host=settings.RSPAMD_HOST,
                    port=settings.RSPAMD_PORT,
                    password=settings.RSPAMD_CONTROLLER_PASSWORD
                )
            else:
                cls._client = RspamdRspamdcClient()
        return cls._client
    
    @staticmethod
    def learn_message(raw_message: Union[bytes, str], decision: str) -> Dict:
        if not settings.RSPAMD_ENABLED:
            return {"status": "disabled", "message": "Rspamd learning is disabled"}
        
        if decision not in ["spam", "ham"]:
            raise ValueError("Decision must be 'spam' or 'ham'")
        
        client = RspamdService._get_client()
        return client.learn(raw_message, decision)
    
    @staticmethod
    def ping() -> bool:
        if not settings.RSPAMD_ENABLED:
            return False
        try:
            client = RspamdService._get_client()
            return client.ping()
        except Exception:
            return False
    
    @staticmethod
    def get_status() -> dict:
        if not settings.RSPAMD_ENABLED:
            return {"enabled": False}
        try:
            client = RspamdService._get_client()
            return client.get_status()
        except Exception as e:
            return {"enabled": True, "error": str(e)}
