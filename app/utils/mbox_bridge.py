from __future__ import annotations

import mailbox
import hashlib
from pathlib import Path
from typing import Dict
import glob


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

    try:
        mbox = mailbox.mbox(str(source))
    except (PermissionError, OSError):
        return {
            "scanned": 0,
            "imported": 0,
            "already_known": 0,
            "missing_source": 0,
            "permission_denied": 1,
        }

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
        "permission_denied": 0,
    }


def import_mbox_glob(source_glob: str, target_dir: str) -> Dict[str, int]:
    """Import messages from all mbox files matched by source_glob."""
    matched_paths = sorted(glob.glob(source_glob))

    aggregated = {
        "sources_matched": len(matched_paths),
        "sources_processed": 0,
        "sources_skipped": 0,
        "sources_permission_denied": 0,
        "scanned": 0,
        "imported": 0,
        "already_known": 0,
        "missing_source": 0,
        "permission_denied": 0,
    }

    for path in matched_paths:
        source = Path(path)

        # Skip non-regular files and mbox lock helpers.
        if not source.is_file() or source.name.endswith('.lock'):
            aggregated["sources_skipped"] += 1
            continue

        result = import_mbox_messages(str(source), target_dir)
        aggregated["sources_processed"] += 1
        aggregated["scanned"] += result.get("scanned", 0)
        aggregated["imported"] += result.get("imported", 0)
        aggregated["already_known"] += result.get("already_known", 0)
        aggregated["missing_source"] += result.get("missing_source", 0)
        denied = result.get("permission_denied", 0)
        aggregated["permission_denied"] += denied
        if denied:
            aggregated["sources_permission_denied"] += 1

    return aggregated
