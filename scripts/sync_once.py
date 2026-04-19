from __future__ import annotations

from datetime import datetime, timezone
from app.db import SessionLocal
from app.config import settings
from app.services.settings_service import SettingsService
from app.utils.message_sync import MessageSyncService
from app.utils.mbox_bridge import import_mbox_messages, import_mbox_glob


def main() -> None:
    mailbox_bridge_enabled = settings.MAILBOX_BRIDGE_ENABLED
    mailbox_source_glob = settings.MAILBOX_SOURCE_GLOB.strip()
    mailbox_source_path = settings.MAILBOX_SOURCE_PATH
    local_eml_path = settings.MAIL_SOURCE_PATH

    if mailbox_bridge_enabled:
        if mailbox_source_glob:
            bridge_result = import_mbox_glob(mailbox_source_glob, local_eml_path)
        elif os.path.isdir(mailbox_source_path):
            bridge_result = import_mbox_glob(os.path.join(mailbox_source_path, "*"), local_eml_path)
        else:
            bridge_result = import_mbox_messages(mailbox_source_path, local_eml_path)
        print({"mailbox_bridge": bridge_result})

    db = SessionLocal()
    try:
        sync_result = MessageSyncService.sync_messages_from_provider(db)
        SettingsService.set_setting(db, "last_sync_new_messages", str(sync_result.get("new_messages", 0)))
        SettingsService.set_setting(db, "last_sync_duplicates", str(sync_result.get("duplicates_skipped", 0)))
        SettingsService.set_setting(db, "last_sync_total", str(sync_result.get("total", 0)))
        SettingsService.set_setting(db, "last_sync_at", datetime.now(timezone.utc).isoformat())
        print(sync_result)
    finally:
        db.close()


if __name__ == "__main__":
    main()
