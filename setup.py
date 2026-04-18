#!/usr/bin/env python
"""
Setup script for RspamdHotOrNot
"""
from setuptools import setup, find_packages

setup(
    name="rspamd-hot-or-not",
    version="1.0.0",
    description="Web-based mail classification tool for Rspamd learning",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/rspamd-hot-or-not",
    packages=find_packages(exclude=["tests", "data"]),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "sqlalchemy==2.0.23",
        "python-dotenv==1.0.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.6",
        "email-validator==2.1.0",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "requests==2.31.0",
        "aiofiles==23.2.1",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-cov==4.1.0",
            "black==23.12.0",
            "flake8==6.1.0",
        ],
    },
)
