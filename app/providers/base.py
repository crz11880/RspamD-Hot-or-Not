from abc import ABC, abstractmethod
from typing import Optional, List

class MessageProvider(ABC):
    
    @abstractmethod
    def list_pending_messages(self) -> List[dict]:
        pass
    
    @abstractmethod
    def get_message(self, provider_id: str) -> Optional[dict]:
        pass
    
    @abstractmethod
    def get_raw_message(self, provider_id: str) -> Optional[bytes]:
        pass
    
    @abstractmethod
    def mark_processed(self, provider_id: str, status: str):
        pass
    
    @abstractmethod
    def skip_message(self, provider_id: str):
        pass
