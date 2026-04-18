# RspamdHotOrNot

Eine moderne, einfache Webanwendung für manuelle Spam-Klassifizierung und Rspamd-Training.

## Features

- 🎯 **Einfache Web-UI** für schnelle Mail-Klassifizierung
- 📊 **Dashboard** mit Statistiken und Aktivitätslog
- 🔐 **Authentifizierung** mit Session-basiertem Login
- 💾 **SQLite Datenbank** für lokale Speicherung
- 🏗️ **Modulare Architektur** mit Provider-Abstraktion
- 🐳 **Docker-ready** für einfache Bereitstellung
- ⌨️ **Tastaturkürzel** für schnelle Bedienung (S, H, U)
- 📧 **Volle Raw-Mail-Unterstützung** für Rspamd-Training
- 🔄 **Mail-Duplikaterkennung** basierend auf Hash

## Technologie-Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (kein Framework)
- **Templates**: Jinja2
- **Datenbank**: SQLite
- **Containerisierung**: Docker & Docker Compose
- **Authentifizierung**: Passlib (bcrypt)

## Installation (fuer Anfaenger)

Diese Anleitung ist absichtlich simpel gehalten. Wenn du nur starten willst, kopiere die Befehle genau in dieser Reihenfolge.

### Variante A: Lokaler Start auf deinem Rechner (empfohlen zum Ausprobieren)

Voraussetzungen:
- Git
- Python 3.11+

```bash
# 1) Repository klonen
git clone https://github.com/crz11880/RspamD-Hot-or-Not.git
cd RspamD-Hot-or-Not

# 2) Virtuelle Python-Umgebung anlegen und aktivieren
python3 -m venv .venv
source .venv/bin/activate

# 3) Abhaengigkeiten installieren
pip install --upgrade pip
pip install -r requirements.txt

# 4) .env erzeugen
cp .env.example .env

# 5) App starten
make run
```

Danach im Browser oeffnen:
- `http://127.0.0.1:8000`

Standard-Login:
- Benutzername: `admin`
- Passwort: `password123`

Wichtig nach dem ersten Login:
- In den Einstellungen sofort Benutzername/Passwort aendern.

### Variante B: Installation auf Linux-Server mit Rspamd

```bash
# 1) Basis-Pakete
sudo apt update
sudo apt install -y git python3 python3-venv make rspamd-client

# 2) Projekt holen
git clone https://github.com/crz11880/RspamD-Hot-or-Not.git
cd RspamD-Hot-or-Not

# 3) Installer ausfuehren
bash install.sh

# 4) Konfiguration
cp .env.example .env
```

In `.env` mindestens diese Werte setzen:

```ini
RSPAMD_ENABLED=True
LEARN_COMMAND_TYPE=rspamc
RSPAMD_HOST=127.0.0.1
RSPAMD_PORT=11333

MAIL_SOURCE_TYPE=local_eml
MAIL_SOURCE_PATH=./data/emails
MAILBOX_BRIDGE_ENABLED=True
MAILBOX_SOURCE_PATH=/var/mail/<dein-user>
```

Dann starten:

```bash
make run
```

Im Browser oeffnen:
- `http://SERVER-IP:8000`

Wenn der Browser die Seite nicht erreicht:
- Port `8000` in Firewall/Sicherheitsgruppe freigeben.

### Schneller Funktionstest (2 Minuten)

1. Login mit Standarddaten.
2. Dashboard oeffnen.
3. Auf `Mails synchronisieren` klicken.
4. Zu `Review` wechseln und pruefen, ob Mails angezeigt werden.

Wenn keine neuen Mails erscheinen:
- Pruefen, ob nur Duplikate angekommen sind (werden bewusst uebersprungen).
- Pruefen, ob `MAILBOX_SOURCE_PATH` korrekt ist.

Fuer ausfuehrliche Installationsoptionen siehe [INSTALL.md](INSTALL.md).

## Konfiguration

### .env Datei

```ini
# Anwendung
DEBUG=False
SECRET_KEY=sehr-langes-zufälliges-string-in-produktion

# Datenbank
DATABASE_URL=sqlite:///data/db/rspamd_learning.db

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=password123

# Mail-Quelle
MAIL_SOURCE_TYPE=local_eml
MAIL_SOURCE_PATH=./data/emails
MAILBOX_BRIDGE_ENABLED=True
MAILBOX_SOURCE_PATH=/var/mail/hwlmadm

# Rspamd (Optional)
RSPAMD_ENABLED=False
RSPAMD_HOST=127.0.0.1
RSPAMD_PORT=11333
LEARN_COMMAND_TYPE=rspamc
```

## Verwendung

### 1. Mails vorbereiten

Platzieren Sie .eml-Dateien im konfigurierten `MAIL_SOURCE_PATH` (Standard: `./data/emails`).

Beispiel:
```
data/emails/
├── mail1.eml
├── mail2.eml
└── mail3.eml
```

### 1a. Automatischer Import aus System-Mailbox (Server)

Wenn eingehende Mails auf dem Server als mbox-Datei landen (z.B. `/var/mail/hwlmadm`),
kann der Auto-Sync diese automatisch nach `MAIL_SOURCE_PATH` als `.eml` importieren.

Empfohlene `.env`-Werte:

```ini
MAIL_SOURCE_TYPE=local_eml
MAIL_SOURCE_PATH=./data/emails
MAILBOX_BRIDGE_ENABLED=True
MAILBOX_SOURCE_PATH=/var/mail/hwlmadm
```

Damit erscheinen neue Server-Mails ohne manuellen Datei-Upload im Tool.

### 2. Im Dashboard synchronisieren

1. Login mit Admin-Credentials
2. Dashboard öffnen
3. Button "Mails synchronisieren" klicken
4. Zur Prüfseite wechseln

### 3. Mails klassifizieren

**Prüfseite** zeigt eine Mail:
- Absender, Empfänger, Betreff
- Body-Vorschau (erste 2000 Zeichen)
- Drei Buttons: **Spam**, **Kein Spam**, **Überspringen**

**Tastaturkürzel**:
- `S` = Als Spam markieren
- `H` = Als Ham (nicht-Spam) markieren
- `U` = Überspringen

### 4. Verlauf ansehen

**Verlauf-Seite** zeigt alle klassifizierten Mails mit:
- Datum/Uhrzeit
- Absender
- Betreff
- Entscheidung
- Rspamd-Submit-Status

## Rspamd-Integration

### Mit HTTP-API (empfohlen)

```bash
RSPAMD_ENABLED=True
RSPAMD_HOST=rspamd.example.com
RSPAMD_PORT=11333
RSPAMD_CONTROLLER_PASSWORD=your_password
LEARN_COMMAND_TYPE=http
```

### Mit rspamc CLI

```bash
RSPAMD_ENABLED=True
LEARN_COMMAND_TYPE=rspamc
```

Stelle sicher, dass `rspamc` installiert ist:
```bash
apt-get install rspamd-client  # Debian/Ubuntu
brew install rspamd            # macOS
```

## Projektstruktur

```
app/
├── main.py              # FastAPI Entry Point
├── config.py            # Konfiguration (Settings)
├── db.py                # SQLAlchemy Setup
│
├── models/              # SQLAlchemy ORM Models
│   ├── user.py
│   ├── message.py
│   ├── classification.py
│   ├── settings.py
│   └── audit_log.py
│
├── schemas/             # Pydantic Schemas (API)
│   ├── user.py
│   ├── message.py
│   ├── classification.py
│   └── settings.py
│
├── services/            # Business Logic
│   ├── auth_service.py
│   ├── classification_service.py
│   ├── rspamd_service.py
│   ├── audit_log_service.py
│   └── settings_service.py
│
├── providers/           # Mail Provider Abstraction
│   ├── base.py          # Basis-Interface
│   ├── local_eml.py     # LocalEml Implementation
│   └── factory.py       # Provider Factory
│
├── routes/              # API Endpoints
│   ├── auth.py
│   ├── messages.py
│   ├── dashboard.py
│   ├── settings.py
│   └── admin.py
│
├── templates/           # Jinja2 HTML Templates
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── review.html
│   ├── history.html
│   └── settings.html
│
├── static/              # Frontend Assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       └── review.js
│
└── utils/               # Utilities
    ├── security.py      # Auth & Session Management
    ├── rspamd_client.py # Rspamd HTTP/CLI Clients
    ├── message_sync.py  # Mail Sync Service
    └── mbox_bridge.py   # Import von mbox nach .eml

scripts/
└── sync_once.py         # One-shot Sync (Timer/Service)

data/
├── db/                  # SQLite Database
└── emails/              # Source EML Files
    ├── mail1.eml
    └── processed/       # Verarbeitete Mails
        ├── spam/
        ├── ham/
        └── skipped/
```

## Datenbank-Schema

### users
```sql
id | username | hashed_password | is_active | created_at | updated_at
```

### messages
```sql
id | provider_id | provider_type | sender | recipient | subject | received_date | raw_message | message_hash | status | score | source_path | created_at | updated_at
```

### classifications
```sql
id | message_id | user_id | decision | rspamd_submit_status | rspamd_response | created_at
```

### settings
```sql
id | key | value | created_at | updated_at
```

### audit_log
```sql
id | user_id | action | resource_type | resource_id | details | created_at
```

## API Endpoints

### Auth
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Aktuelle Benutzerinfo
- `POST /api/auth/logout` - Logout

### Messages
- `GET /api/messages/pending` - Alle offenen Mails
- `GET /api/messages/next` - Nächste Mail
- `GET /api/messages/{id}` - Mail-Details
- `POST /api/messages/{id}/classify` - Mail klassifizieren
- `POST /api/messages/{id}/skip` - Mail überspringen
- `GET /api/messages/history/list` - Klassifizierungsverlauf

### Dashboard
- `GET /api/dashboard/stats` - Dashboard-Statistiken
- `GET /api/dashboard/recent-activities` - Letzte Aktivitäten
- `POST /api/dashboard/sync-messages` - Mails synchronisieren

### Settings
- `GET /api/settings` - Alle Einstellungen
- `GET /api/settings/{key}` - Einzelne Einstellung
- `PUT /api/settings/{key}` - Einstellung aktualisieren

### Admin
- `POST /api/admin/init-database` - DB initialisieren
- `POST /api/admin/sync-emails` - Mails synchronisieren
- `POST /api/admin/upload-email` - Email hochladen

## Entwicklung

### Neue Provider hinzufügen

1. Erstelle `app/providers/imap_provider.py`:

```python
from app.providers.base import MessageProvider

class IMAPProvider(MessageProvider):
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
    
    def list_pending_messages(self):
        # Implement IMAP logic
        pass
    
    # ... weitere Methoden
```

2. Aktualisiere `app/providers/factory.py`:

```python
elif settings.MAIL_SOURCE_TYPE == "imap":
    return IMAPProvider(...)
```

### Rspamd-Anbindung erweitern

Die Rspamd-Integration befindet sich in:
- `app/services/rspamd_service.py`
- `app/utils/rspamd_client.py`

Um eine neue Methode hinzuzufügen:

```python
class RspamdService:
    @staticmethod
    def get_reputation(sender):
        client = RspamdService._get_client()
        return client.get_reputation(sender)
```

## Sicherheit

- ✅ Passwörter mit bcrypt gehasht
- ✅ Session-basierte Authentifizierung
- ✅ Secret Key in .env (nicht im Code)
- ✅ Eingabe-Validierung mit Pydantic
- ⚠️ CSRF-Schutz: Wird noch hinzugefügt
- ⚠️ Rate Limiting: Optional via Middleware

## Performance-Tipps

- **DB-Indizes** sind auf wichtigen Feldern gesetzt
- **Paginierung** auf History-Seite aktiv
- **Message Preview** begrenzt auf 2000 Zeichen
- **Duplikat-Check** mittels SHA256-Hash

## Troubleshooting

### "No pending messages"

1. Stelle sicher, dass .eml-Dateien im korrekten Pfad liegen
2. Klick Dashboard → "Mails synchronisieren"
3. Überprüfe `data/emails/` Ordner
4. Bei Serverbetrieb mit mbox: `MAILBOX_BRIDGE_ENABLED=True` und `MAILBOX_SOURCE_PATH` prüfen

### Rspamd-Verbindung fehlgeschlagen

1. Überprüfe `RSPAMD_ENABLED` in .env
2. Überprüfe Host und Port
3. Test mit: `rspamc ping`

### SQLite Database locked

1. Stelle sicher, dass kein anderer Prozess die DB nutzt
2. Lösche `data/db/*.db` und starte neu

## Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

## Beitragen

Beiträge sind willkommen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Richtlinien.

## Support & Community

- **Issues**: GitHub Issues für Bugs und Features
- **Diskussionen**: GitHub Discussions für Fragen
- **Documentation**: [INSTALL.md](INSTALL.md), [CONTRIBUTING.md](CONTRIBUTING.md)
- **Support the Project**: [Buy Me a Coffee](https://buymeacoffee.com/worklessit)

## Versionshistorie

Siehe [CHANGELOG.md](CHANGELOG.md) für alle Änderungen.

## Disclaimer

Diese Software wird ohne Gewährleistung bereitgestellt. Siehe LICENSE für Details.
