# Installation Guide - RspamdHotOrNot

Diese Anleitung ist fuer Einsteiger geschrieben.
Wenn du die Schritte der Reihe nach ausfuehrst, laeuft die App in wenigen Minuten.

## 1. Schnellstart (lokal, empfohlen)

Voraussetzungen:
- Git
- Python 3.11+

### Schritt 1: Repository klonen

```bash
git clone https://github.com/crz11880/RspamD-Hot-or-Not.git
cd RspamD-Hot-or-Not
```

### Schritt 2: Python-Umgebung erstellen

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Schritt 3: Abhaengigkeiten installieren

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Schritt 4: Konfiguration anlegen

```bash
cp .env.example .env
```

### Schritt 5: App starten

```bash
make run
```

### Schritt 6: Im Browser oeffnen

- http://127.0.0.1:8000

Standard-Login:
- Benutzername: admin
- Passwort: password123

Direkt danach in den Einstellungen die Zugangsdaten aendern.

---

## 2. Linux-Server Installation (mit Rspamd)

Diese Variante ist fuer einen Server gedacht, auf dem Rspamd bereits vorhanden ist.

### Schritt 1: Pakete installieren

```bash
sudo apt update
sudo apt install -y git python3 python3-venv make rspamd-client
```

### Schritt 2: Repository klonen

```bash
git clone https://github.com/crz11880/RspamD-Hot-or-Not.git
cd RspamD-Hot-or-Not
```

### Schritt 3: Projekt installieren

```bash
bash install.sh
```

### Schritt 4: .env anlegen

```bash
cp .env.example .env
```

### Schritt 5: Mindestkonfiguration setzen

In .env diese Werte eintragen:

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

### Schritt 6: App starten

```bash
make run
```

Wenn noetig Port 8000 in der Firewall freigeben.

---

## 3. Production mit systemd (bewaehrtes Setup)

### 3.1 App-Service

Datei: /etc/systemd/system/rspamd-hot-or-not.service

```ini
[Unit]
Description=RspamdHotOrNot FastAPI Service
After=network.target

[Service]
Type=simple
User=hwlmadm
WorkingDirectory=/home/hwlmadm/rspamd-hot-or-not
Environment=APP_HOST=0.0.0.0
Environment=APP_PORT=8000
ExecStart=/home/hwlmadm/rspamd-hot-or-not/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 3.2 Auto-Sync Service

Datei: /etc/systemd/system/rspamd-hot-or-not-sync.service

```ini
[Unit]
Description=RspamdHotOrNot Auto Sync Once
After=network.target

[Service]
Type=oneshot
User=hwlmadm
WorkingDirectory=/home/hwlmadm/rspamd-hot-or-not
Environment=PYTHONPATH=/home/hwlmadm/rspamd-hot-or-not
ExecStart=/home/hwlmadm/rspamd-hot-or-not/venv/bin/python /home/hwlmadm/rspamd-hot-or-not/scripts/sync_once.py
```

### 3.3 Auto-Sync Timer

Datei: /etc/systemd/system/rspamd-hot-or-not-sync.timer

```ini
[Unit]
Description=Run RspamdHotOrNot auto sync every minute

[Timer]
OnBootSec=1min
OnUnitActiveSec=1min
Persistent=true

[Install]
WantedBy=timers.target
```

### 3.4 Aktivieren

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now rspamd-hot-or-not.service
sudo systemctl enable --now rspamd-hot-or-not-sync.timer
sudo systemctl start rspamd-hot-or-not-sync.service
```

### 3.5 Status pruefen

```bash
systemctl status rspamd-hot-or-not.service --no-pager -l
systemctl list-timers --no-pager | grep rspamd-hot-or-not-sync
journalctl -u rspamd-hot-or-not-sync.service -n 30 --no-pager
```

---

## 4. Erster Funktionstest (2 Minuten)

1. Login mit admin / password123.
2. Dashboard oeffnen.
3. Mails synchronisieren klicken.
4. Zu Review wechseln und pruefen, ob neue Nachrichten angezeigt werden.

Hinweis:
- Duplikate werden absichtlich nicht als neue Mails gezaehlt.

---

## 5. Update von GitHub

```bash
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```

Bei systemd-Deployments anschliessend:

```bash
sudo systemctl restart rspamd-hot-or-not.service
sudo systemctl start rspamd-hot-or-not-sync.service
```

---

## 6. Typische Fehler und Loesungen

### Fehler: ModuleNotFoundError

Loesung:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Fehler: Port 8000 belegt

Loesung:

```bash
lsof -i :8000
kill -9 <PID>
```

Oder anderen Port verwenden.

### Fehler: Keine neuen Mails sichtbar

Pruefen:
- Stimmt MAILBOX_SOURCE_PATH?
- Laeuft der sync timer?
- Sind neue Mails eventuell Duplikate?

Hilfreiche Befehle:

```bash
systemctl list-timers --no-pager | grep rspamd-hot-or-not-sync
journalctl -u rspamd-hot-or-not-sync.service -n 50 --no-pager
```

### Fehler: Rspamd nicht erreichbar

Pruefen:

```bash
rspamc ping
```

Und in .env:

```ini
RSPAMD_ENABLED=True
LEARN_COMMAND_TYPE=rspamc
RSPAMD_HOST=127.0.0.1
RSPAMD_PORT=11333
```

---

## 7. Sicherheit fuer Produktion

Vor einem echten Internet-Deploy unbedingt:
- ADMIN Passwort aendern
- SECRET_KEY ersetzen
- DEBUG=False setzen
- Reverse Proxy mit HTTPS nutzen (z. B. nginx)

Secret erzeugen:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```
