#!/usr/bin/env python3
"""
========================================
  Configuration File
  Author  : Sachin Kumar
  Email   : sachinyadav2063@gmail.com
  Project : Web Security Learning Project

  Centralized configuration for the Flask app
========================================
"""

import os
import secrets

# ─────────────────────────────────────────
#  FLASK CONFIGURATION
# ─────────────────────────────────────────

# Secret key for session management
# In production, load this from environment or .env file
SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))

# Database configuration
DATABASE_FILE = os.getenv('DATABASE_FILE', 'demo.db')

# Flask debug mode (should be False in production)
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Server host and port
HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 5000))

# ─────────────────────────────────────────
#  SECURITY SETTINGS
# ─────────────────────────────────────────

# Session configuration
SESSION_COOKIE_SECURE = True  # Only send over HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection

# Security headers
SECURITY_HEADERS = {
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Referrer-Policy': 'no-referrer',
    'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
    'X-XSS-Protection': '1; mode=block',
}

# ─────────────────────────────────────────
#  DEMO USER CREDENTIALS (for testing only)
# ─────────────────────────────────────────

DEMO_USERS = [
    {
        'username': 'admin',
        'password': 'admin123',
        'role': 'admin'
    },
    {
        'username': 'sachin',
        'password': 'password1',
        'role': 'user'
    },
    {
        'username': 'user',
        'password': 'user1234',
        'role': 'user'
    }
]
