# Installation Guide - RspamdHotOrNot

## Schnellstart von GitHub

### 1. Clone des Repositories

```bash
git clone https://github.com/yourusername/rspamd-hot-or-not.git
cd rspamd-hot-or-not
```

### 2. Installation (automatisch)

#### macOS/Linux:
```bash
chmod +x install.sh
./install.sh
```

#### Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
```

### 3. Konfiguration

Bearbeiten Sie die `.env`-Datei:
```bash
nano .env
```

Wichtige Einstellungen:
- `SECRET_KEY`: Ändern Sie zu einem sicheren Wert
- `ADMIN_PASSWORD`: Ändern Sie das Standard-Passwort
- `MAIL_SOURCE_PATH`: Pfad zu Ihren .eml-Dateien
- `RSPAMD_ENABLED`: Setzen Sie auf `True` wenn Rspamd verfügbar ist

### 4. Start der Anwendung

#### Development-Modus (mit Auto-Reload):
```bash
make run-dev
# oder manuell:
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

#### Production-Modus:
```bash
make run
# oder manuell:
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Zugriffsadresse: **http://localhost:8000**

---

## Detaillierte Installation

### Schritt 1: Git installieren

Falls nicht vorhanden:
- **macOS**: `brew install git`
- **Ubuntu/Debian**: `apt-get install git`
- **Windows**: https://git-scm.com/download/win

### Schritt 2: Repository klonen

```bash
git clone https://github.com/yourusername/rspamd-hot-or-not.git
cd rspamd-hot-or-not
```

### Schritt 3: Python Environment

```bash
# Python 3.9+ erforderlich
python3 --version

# Virtual Environment erstellen
python3 -m venv venv

# Aktivieren
source venv/bin/activate          # macOS/Linux
# oder
venv\Scripts\activate.bat         # Windows CMD
# oder
venv\Scripts\Activate.ps1         # Windows PowerShell
```

### Schritt 4: Abhängigkeiten installieren

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Schritt 5: Umgebungsvariablen

```bash
cp .env.example .env
nano .env  # Bearbeiten Sie die Einstellungen
```

### Schritt 6: Datenbank vorbereiten

```bash
mkdir -p data/db data/emails
python -c "from app.db import init_db; init_db()"
```

### Schritt 7: Start

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Mit Docker

### Voraussetzungen
- Docker: https://docker.com/get-started
- Docker Compose: Normalerweise mit Docker enthalten

### Installation

```bash
git clone https://github.com/yourusername/rspamd-hot-or-not.git
cd rspamd-hot-or-not

# Mit Rspamd-Integration
docker-compose up -d

# Oder nur die App
docker build -t rspamd-learning .
docker run -p 8000:8000 -v $(pwd)/data:/app/data rspamd-learning
```

Zugriffsadresse: **http://localhost:8000**

### Logs ansehen

```bash
docker-compose logs -f app
```

### Container stoppen

```bash
docker-compose down
```

---

## Systemanforderungen

### Minimum
- **Python**: 3.9+
- **RAM**: 256 MB
- **Disk**: 100 MB
- **OS**: Linux, macOS, Windows

### Empfohlen
- **Python**: 3.11+
- **RAM**: 512 MB
- **Disk**: 1 GB (für Mails)
- **OS**: Linux (für Production)

---

## Makefile Commands

Nach Installation können Sie diese Befehle nutzen:

```bash
make help              # Alle verfügbaren Befehle anzeigen
make run              # Produktions-Server starten
make run-dev          # Development-Server mit Reload starten
make test             # Tests ausführen
make lint             # Code-Qualitätsprüfung
make format           # Code formatieren
make docker-up        # Docker Compose starten
make docker-down      # Docker Compose stoppen
make clean            # Cache löschen
```

---

## Erste Schritte

### 1. Test-Mails hinzufügen

```bash
# Im Projekt-Verzeichnis befinden sich bereits Test-Mails:
ls data/emails/*.eml
```

Oder neue .eml-Dateien hinzufügen:
```bash
cp your-email.eml data/emails/
```

### 2. Dashboard aufrufen

1. Browser: http://localhost:8000
2. Login: `admin` / `password123`
3. Dashboard → "Mails synchronisieren"
4. Zur Prüfseite wechseln

### 3. Mails klassifizieren

- **Spam**: Klick "Spam" oder Taste `S`
- **Kein Spam**: Klick "Kein Spam" oder Taste `H`
- **Überspringen**: Klick "Überspringen" oder Taste `U`

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"

**Lösung**: Virtual Environment wurde nicht aktiviert
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Port 8000 already in use"

**Lösung**: Port ändern oder anderen Prozess stoppen
```bash
# Anderen Port nutzen:
python -m uvicorn app.main:app --port 8001

# Oder Prozess auf Port 8000 finden:
lsof -i :8000
kill -9 <PID>
```

### "Database is locked"

**Lösung**: Andere Prozesse schließen oder DB zurücksetzen
```bash
make db-reset
# oder manuell:
rm -f data/db/*.db
python -c "from app.db import init_db; init_db()"
```

### Rspamd-Verbindung funktioniert nicht

**Überprüfung**:
```bash
# Test mit rspamc:
rspamc ping

# Test mit HTTP:
curl http://rspamd-host:11333/stat
```

**In .env setzen**:
```ini
RSPAMD_ENABLED=True
RSPAMD_HOST=your-rspamd-host
RSPAMD_PORT=11333
LEARN_COMMAND_TYPE=rspamc
```

---

## Sicherheit in Production

### Kritische Änderungen vor dem Deploy

1. **SECRET_KEY** ändern:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. **Admin-Passwort** ändern:
```bash
# In .env oder nach Login über Benutzer-API
```

3. **DEBUG deaktivieren**:
```ini
DEBUG=False
```

4. **HTTPS** aktivieren (reverse proxy empfohlen):
```bash
# Beispiel mit nginx
```

### Deployment mit Supervisor (Production)

`/etc/supervisor/conf.d/rspamd-learning.conf`:
```ini
[program:rspamd-learning]
directory=/path/to/rspamd-hot-or-not
command=/path/to/rspamd-hot-or-not/venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
autostart=true
autorestart=true
user=www-data
environment=PATH="/path/to/venv/bin"
stdout_logfile=/var/log/rspamd-learning.log
```

### Deployment mit Systemd (Production)

`/etc/systemd/system/rspamd-learning.service`:
```ini
[Unit]
Description=RspamdHotOrNot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/rspamd-hot-or-not
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable rspamd-learning
sudo systemctl start rspamd-learning
sudo systemctl status rspamd-learning
```

---

## Updates von GitHub

```bash
# Neueste Version holen
git pull origin main

# Dependencies aktualisieren
pip install -r requirements.txt --upgrade

# Datenbank-Migrationen durchführen (falls vorhanden)
# python -m alembic upgrade head

# Neu starten
make run
```

---

## Support & Debugging

### Logs ansehen

```bash
# Terminal während Laufzeit beobachten
tail -f /var/log/rspamd-learning.log

# Oder während Development:
python -m uvicorn app.main:app --log-level debug
```

### Debug-Informationen

```bash
# Python Version
python --version

# Installed packages
pip list

# Datenbank überprüfen
sqlite3 data/db/rspamd_learning.db ".tables"

# API-Test
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/messages/pending
```

---

## Nächste Schritte

1. ✅ Installation
2. ✅ Konfiguration
3. 📧 Test-Mails vorbereiten
4. 🔗 Rspamd verbinden (optional)
5. 👥 Weitere Benutzer hinzufügen
6. 🔒 HTTPS einrichten
7. 📊 Monitoring aufsetzen

Viel Erfolg!
