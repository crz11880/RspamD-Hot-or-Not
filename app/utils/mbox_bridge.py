from __future__ import annotations

import mailbox
import hashlib
from pathlib import Path
from typing import Dict


def import_mbox_messages(mbox_path: str, target_dir: str) -> Dict[str, int]:
    """Import messages from an mbox file into target_dir as .eml files.

    Filenames are deterministic (sha256-based), so repeated runs are idempotent.
    """
    source = Path(mbox_path)
    inbox = Path(target_dir)
    processed = inbox / "processed"

    inbox.mkdir(parents=True, exist_ok=True)
    (processed / "spam").mkdir(parents=True, exist_ok=True)
    (processed / "ham").mkdir(parents=True, exist_ok=True)
    (processed / "skipped").mkdir(parents=True, exist_ok=True)

    if not source.exists() or not source.is_file():
        return {"scanned": 0, "imported": 0, "already_known": 0, "missing_source": 1}

    scanned = 0
    imported = 0
    already_known = 0

    mbox = mailbox.mbox(str(source))
    for _, msg in mbox.iteritems():
        scanned += 1
        raw = msg.as_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        filename = f"mbox_{digest}.eml"

        candidate_paths = [
            inbox / filename,
            processed / "spam" / filename,
            processed / "ham" / filename,
            processed / "skipped" / filename,
        ]

        if any(path.exists() for path in candidate_paths):
            already_known += 1
            continue

        (inbox / filename).write_bytes(raw)
        imported += 1

    return {
        "scanned": scanned,
        "imported": imported,
        "already_known": already_known,
        "missing_source": 0,
    }
