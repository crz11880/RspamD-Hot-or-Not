# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-18

### Added
- Initial release
- Web-based UI for mail classification
- Dashboard with statistics
- SQLite database for local storage
- LocalEML provider for file-based emails
- Rspamd integration (HTTP and CLI)
- Session-based authentication
- Audit logging
- Keyboard shortcuts (S, H, U)
- Docker support with Docker Compose
- Comprehensive documentation
- GitHub Actions CI/CD

### Features
- Login system with bcrypt hashing
- Mail preview with sender, subject, body
- Classify emails as Spam or Ham
- Skip emails for later review
- View classification history
- Dashboard with pending/classified stats
- Settings panel
- Database synchronization

### Technical
- FastAPI backend
- Vanilla JavaScript frontend
- Jinja2 templating
- SQLAlchemy ORM
- Pydantic validation

---

## [Unreleased]

### Planned
- IMAP provider support
- Multiple user accounts
- Email attachment preview
- CSRF token protection
- Rate limiting
- API documentation (Swagger)
- Rspamd webhook integration
- Export/Import functionality
- Dark mode toggle
- Advanced search
- Batch operations
