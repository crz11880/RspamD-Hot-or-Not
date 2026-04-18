# RspamdHotOrNot GitHub Setup

Diese Anleitung hilft Ihnen, das Projekt auf GitHub zu veröffentlichen.

## Schritt 1: GitHub Repository erstellen

1. Gehen Sie zu https://github.com/new
2. Repository-Name: `rspamd-hot-or-not`
3. Beschreibung: "Web-based mail classification tool for Rspamd learning"
4. Wählen Sie: **Public** (falls Sie möchten, dass andere beitragen)
5. Klicken Sie: "Create repository"

## Schritt 2: Lokales Repo initialisieren und pushen

```bash
cd /Users/christian/Git/RspamD\ Hot\ or\ Not

# Falls nicht bereits ein Git Repo:
git init

# Oder falls bereits ein Repo existiert:
git status

# Remote hinzufügen (ersetzen Sie mit Ihrer URL)
git remote add origin https://github.com/yourusername/rspamd-hot-or-not.git

# Branch in main umbenennen (falls nötig)
git branch -M main

# Alle Dateien hinzufügen
git add .

# Initial commit
git commit -m "Initial commit: RspamdHotOrNot v1.0.0"

# Zum Repository pushen
git push -u origin main
```

## Schritt 3: GitHub Einstellungen

### Branch Protection (optional aber empfohlen)

1. Gehen Sie zu: Settings → Branches
2. "Add rule" für `main` branch
3. Aktivieren Sie:
   - "Require pull request reviews"
   - "Require status checks to pass"
   - "Dismiss stale pull request approvals"

### Secrets (für Actions)

1. Settings → Secrets and variables → Actions
2. Falls Sie später Code Scanning oder andere automatisierte Tools nutzen möchten

## Schritt 4: GitHub Pages (optional für Doku)

1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: main, folder: /docs (später)

## README.md anpassen

Ersetzen Sie die GitHub-Links in der `README.md`:

```md
# RspamdHotOrNot

...

[project](https://github.com/yourusername/rspamd-hot-or-not)
Repository: https://github.com/yourusername/rspamd-hot-or-not.git
```

## Schritt 5: Releases und Tags

Nachdem Sie gepusht haben:

```bash
# Tag erstellen für v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"

# Tags pushen
git push origin --tags
```

Auf GitHub:
1. Gehen Sie zu: Releases → "Create a new release"
2. Tag: v1.0.0
3. Title: "RspamdHotOrNot v1.0.0"
4. Description: (kopieren Sie aus CHANGELOG.md)
5. "Publish release"

## Schritt 6: Weitere Dateien für GitHub

### README-Abschnitt hinzufügen

```markdown
## Installation

```bash
git clone https://github.com/yourusername/rspamd-hot-or-not.git
cd rspamd-hot-or-not
bash install.sh
```

Siehe [INSTALL.md](INSTALL.md) für detaillierte Anweisungen.
```

### Topics hinzufügen (GitHub UI)

1. Repository-Seite
2. Über "About" auf der Seite rechts
3. Klicken Sie auf Settings-Icon
4. Topics hinzufügen:
   - rspamd
   - mail
   - spam
   - fastapi
   - python

## Schritt 7: CI/CD aktivieren

GitHub Actions sollte automatisch ausgelöst werden:

1. Gehen Sie zu: Actions
2. Sie sollten den "Tests & Linting" Workflow sehen
3. Dieser wird bei jedem Push/PR ausgeführt

## Schritt 8: Zusätzliche GitHub Features (optional)

### Code Scanning
```bash
# Enable in Settings → Security → Code scanning
```

### Dependabot
```bash
# Automatische Dependency Updates
# Settings → Security & analysis → Enable Dependabot
```

## Installation von GitHub für andere

Jetzt können andere Ihr Projekt installieren mit:

```bash
git clone https://github.com/yourusername/rspamd-hot-or-not.git
cd rspamd-hot-or-not
bash install.sh
```

---

## Verwandte Dateien

- [README.md](../README.md) - Hauptdokumentation
- [INSTALL.md](../INSTALL.md) - Installationsanleitung
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Beitragsrichtlinien
- [LICENSE](../LICENSE) - MIT License
- [CHANGELOG.md](../CHANGELOG.md) - Versionshistorie
