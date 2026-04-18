from app.providers.local_eml import LocalEmlProvider
from app.config import settings

def get_provider():
    if settings.MAIL_SOURCE_TYPE == "local_eml":
        return LocalEmlProvider(settings.MAIL_SOURCE_PATH)
    else:
        raise ValueError(f"Unknown provider type: {settings.MAIL_SOURCE_TYPE}")
