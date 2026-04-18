from __future__ import annotations

import os
from datetime import datetime, timezone
from app.db import SessionLocal
from app.services.settings_service import SettingsService
from app.utils.message_sync import MessageSyncService
from app.utils.mbox_bridge import import_mbox_messages


def _enabled(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def main() -> None:
    mailbox_bridge_enabled = _enabled(os.getenv("MAILBOX_BRIDGE_ENABLED", "true"))
    mailbox_source_path = os.getenv("MAILBOX_SOURCE_PATH", "/var/mail/hwlmadm")
    local_eml_path = os.getenv("MAIL_SOURCE_PATH", "./data/emails")

    if mailbox_bridge_enabled:
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
