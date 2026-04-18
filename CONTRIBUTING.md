# Contributing to RspamdHotOrNot

Thank you for your interest in contributing! Here's how you can help:

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/rspamd-hot-or-not.git`
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Follow the setup instructions in [INSTALL.md](INSTALL.md)

## Development

### Code Style

We use:
- **Black** for code formatting (line length: 100)
- **Flake8** for linting
- **Type hints** where practical

```bash
make format
make lint
```

### Testing

Write tests for new features:
```bash
make test
```

### Commit Messages

- Use clear, concise commit messages
- Start with a verb: "Add", "Fix", "Update", "Remove"
- Example: "Add IMAP provider support"

### Pull Requests

1. Update CHANGELOG.md with your changes
2. Ensure all tests pass: `make test`
3. Follow the PR template

## Reporting Issues

Use GitHub Issues with:
- Clear title
- Detailed description
- Steps to reproduce
- Environment info

## Feature Suggestions

Discuss large features as Issues first before submitting PRs.

## License

By contributing, you agree your code will be licensed under MIT.

Thank you! 🎉
