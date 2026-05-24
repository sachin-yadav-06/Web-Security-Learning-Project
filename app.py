#!/usr/bin/env python3
"""
========================================
  Web Security Demo App — Flask
  Author  : Sachin Kumar
  Email   : sachinyadav2063@gmail.com
  Project : Web Security Learning Project

  Demonstrates VULNERABLE vs SECURE code
  for common web vulnerabilities.

  ⚠️  FOR EDUCATIONAL USE ONLY
      Run ONLY on localhost in a lab.
========================================

Install: pip install flask
Run    : python app.py
Open   : http://127.0.0.1:5000
"""

from flask import Flask, request, render_template_string, redirect, url_for, session
import sqlite3
import hashlib
import os
import html
import secrets
from functools import wraps
from config import (
    SECRET_KEY, DATABASE_FILE, DEBUG, HOST, PORT, 
    SECURITY_HEADERS, DEMO_USERS, SESSION_COOKIE_HTTPONLY,
    SESSION_COOKIE_SECURE, SESSION_COOKIE_SAMESITE
)

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Configure session cookies securely
app.config['SESSION_COOKIE_SECURE'] = SESSION_COOKIE_SECURE
app.config['SESSION_COOKIE_HTTPONLY'] = SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = SESSION_COOKIE_SAMESITE

# ─────────────────────────────────────────
#  MIDDLEWARE: ADD SECURITY HEADERS
# ─────────────────────────────────────────
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    return response

# ─────────────────────────────────────────
#  DATABASE SETUP
# ─────────────────────────────────────────
def init_db():
    """Initialize the SQLite database with demo users."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        
        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                salt     TEXT NOT NULL,
                role     TEXT DEFAULT 'user'
            )
        """)
        
        # Create comments table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                user    TEXT,
                comment TEXT
            )
        """)
        
        # Seed demo users (only if table is empty)
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            for user in DEMO_USERS:
                salt = secrets.token_hex(16)  # Generate random salt per user
                password_hash = hashlib.sha256((salt + user['password']).encode()).hexdigest()
                try:
                    cur.execute(
                        "INSERT INTO users (username, password, salt, role) VALUES (?, ?, ?, ?)",
                        (user['username'], password_hash, salt, user['role'])
                    )
                except sqlite3.IntegrityError:
                    pass  # User already exists
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")

# ─────────────────────────────────────────
#  SESSION MANAGEMENT
# ─────────────────────────────────────────
def login_required(f):
    """Decorator to require login for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ─────────────────────────────────────────
#  AUTHENTICATION ENDPOINTS
# ─────────────────────────────────────────
LOGIN_HTML = """
<!DOCTYPE html><html>
<head><title>Secure Login</title>
<style>
  body{font-family:monospace;background:#0a1a0a;color:#eee;padding:30px;}
  input{padding:8px;margin:5px;width:250px;background:#333;color:#fff;border:1px solid #4caf50;}
  button{padding:8px 20px;background:#4caf50;color:#fff;border:none;cursor:pointer;}
  .container{max-width:400px;margin:50px auto;}
  .error{color:#e94560;}
</style></head>
<body>
  <div class="container">
    <h2>🔐 Login</h2>
    <p>Demo credentials:</p>
    <ul>
      <li>admin / admin123</li>
      <li>sachin / password1</li>
      <li>user / user1234</li>
    </ul>
    {% if error %}
    <p class="error">❌ {{ error }}</p>
    {% endif %}
    <form method="POST">
      <label>Username:</label><br>
      <input type="text" name="username" required><br>
      <label>Password:</label><br>
      <input type="password" name="password" required><br><br>
      <button type="submit">Login</button>
    </form>
  </div>
</body></html>
"""

@app.route("/login", methods=["GET", "POST"])
def login():
    """Secure login endpoint."""
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cur = conn.cursor()
            # ✅ SECURE: Parameterized query
            cur.execute("SELECT id, username, salt, role FROM users WHERE username = ?", (username,))
            user = cur.fetchone()
            conn.close()
            
            if user:
                user_id, db_username, salt, role = user
                # Hash the provided password with the stored salt
                password_hash = hashlib.sha256((salt + password).encode()).hexdigest()
                
                # Retrieve and compare with stored hash
                conn = sqlite3.connect(DATABASE_FILE)
                cur = conn.cursor()
                cur.execute("SELECT password FROM users WHERE id = ?", (user_id,))
                stored_hash = cur.fetchone()[0]
                conn.close()
                
                if password_hash == stored_hash:
                    session['user_id'] = user_id
                    session['username'] = db_username
                    session['role'] = role
                    return redirect(url_for('home'))
                else:
                    error = "Invalid username or password"
            else:
                error = "Invalid username or password"
        except Exception as e:
            error = f"Login error: {str(e)}"
    
    return render_template_string(LOGIN_HTML, error=error)

@app.route("/logout")
def logout():
    """Logout endpoint."""
    session.clear()
    return redirect(url_for('login'))

# ─────────────────────────────────────────
#  HOME PAGE
# ─────────────────────────────────────────
HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Web Security Demo — Sachin Kumar</title>
  <style>
    body { font-family: monospace; background: #1a1a2e; color: #eee; padding: 30px; }
    h1   { color: #e94560; }
    h2   { color: #0f3460; background:#16213e; padding:8px; border-left:4px solid #e94560; }
    a    { display:inline-block; margin:8px; padding:10px 20px;
           background:#0f3460; color:#eee; text-decoration:none; border-radius:5px; }
    a:hover { background:#e94560; }
    .warn { background:#3a1a1a; border:1px solid #e94560;
            padding:12px; border-radius:5px; margin:15px 0; }
    .safe { background:#1a3a1a; border:1px solid #4caf50;
            padding:12px; border-radius:5px; margin:15px 0; }
    .author { color:#888; font-size:12px; margin-top:40px; }
    .user-info { color:#4caf50; margin-bottom:20px; }
  </style>
</head>
<body>
  <h1>🛡️ Web Security Learning Demo</h1>
  <p>Author: <strong>Sachin Kumar</strong> | sachinyadav2063@gmail.com</p>
  
  <div class="user-info">
    ✅ Logged in as: <strong>{{ username }}</strong> ({{ role }}) 
    <a href="/logout" style="display:inline;padding:5px 10px;margin-left:10px;">Logout</a>
  </div>

  <div class="warn">
    ⚠️ <strong>WARNING:</strong> This app contains intentionally vulnerable
    endpoints for educational purposes only. Run ONLY on localhost.
  </div>

  <h2>💉 SQL Injection</h2>
  <a href="/sqli/vulnerable">❌ Vulnerable Login</a>
  <a href="/sqli/secure">✅ Secure Login</a>

  <h2>🖊️ Cross-Site Scripting (XSS)</h2>
  <a href="/xss/vulnerable">❌ Vulnerable Comment Box</a>
  <a href="/xss/secure">✅ Secure Comment Box</a>

  <h2>🚪 Broken Access Control (IDOR)</h2>
  <a href="/idor/vulnerable?id=1">❌ Vulnerable User Profile</a>
  <a href="/idor/secure?id=1">✅ Secure User Profile</a>

  <h2>🔐 Authentication Failures</h2>
  <a href="/auth/weak">❌ Weak Auth (MD5)</a>
  <a href="/auth/strong">✅ Strong Auth (SHA-256 + salt)</a>

  <p class="author">
    🔗 GitHub: github.com/sachin-yadav-06/Web-Security-Learning-Project<br>
    📧 sachinyadav2063@gmail.com<br>
    Educational Project — OWASP Top 10 Demo
  </p>
</body>
</html>
"""

@app.route("/")
@login_required
def home():
    """Home page."""
    return render_template_string(
        HOME_HTML,
        username=session.get('username', 'User'),
        role=session.get('role', 'user')
    )

# ─────────────────────────────────────────
#  1. SQL INJECTION — VULNERABLE
# ─────────────────────────────────────────
SQLI_VULN_HTML = """
<!DOCTYPE html><html>
<head><title>Vulnerable Login (SQLi)</title>
<style>
  body{font-family:monospace;background:#1a0a0a;color:#eee;padding:30px;}
  input{padding:8px;margin:5px;width:250px;background:#333;color:#fff;border:1px solid #e94560;}
  button{padding:8px 20px;background:#e94560;color:#fff;border:none;cursor:pointer;}
  .vuln{background:#3a1a1a;border:1px solid #e94560;padding:12px;margin:10px 0;border-radius:5px;}
  .result{background:#333;padding:12px;margin:10px 0;}
  a{color:#e94560;}
</style></head>
<body>
  <h2>❌ Vulnerable Login — SQL Injection Demo</h2>
  <div class="vuln">
    ⚠️ This form is vulnerable to SQL Injection.<br>
    Try payload: <code>' OR '1'='1' --</code> as username
  </div>
  <form method="POST">
    <label>Username:</label><br>
    <input type="text" name="username" placeholder="Try: ' OR '1'='1' --"><br>
    <label>Password:</label><br>
    <input type="password" name="password" value="anything"><br><br>
    <button type="submit">Login</button>
  </form>
  {% if result %}
  <div class="result">{{ result }}</div>
  {% endif %}
  <br><a href="/">← Back</a> | <a href="/sqli/secure">See Secure Version →</a>
</body></html>
"""

@app.route("/sqli/vulnerable", methods=["GET", "POST"])
def sqli_vulnerable():
    """Demonstrate SQL injection vulnerability."""
    result = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # ❌ VULNERABLE: Direct string concatenation — DO NOT DO THIS
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cur = conn.cursor()
            cur.execute(query)    # Dangerous! User input goes straight into query
            user = cur.fetchone()
            conn.close()

            if user:
                result = f"✅ Logged in as: {user[1]} (Role: {user[4]}) — SQLi succeeded!"
            else:
                result = "❌ Login failed."
        except Exception as e:
            result = f"[DB ERROR] {str(e)[:100]} — (Hint: your injection may have broken the syntax)"

    return render_template_string(SQLI_VULN_HTML, result=result)


# ─────────────────────────────────────────
#  1. SQL INJECTION — SECURE
# ─────────────────────────────────────────
SQLI_SECURE_HTML = """
<!DOCTYPE html><html>
<head><title>Secure Login</title>
<style>
  body{font-family:monospace;background:#0a1a0a;color:#eee;padding:30px;}
  input{padding:8px;margin:5px;width:250px;background:#333;color:#fff;border:1px solid #4caf50;}
  button{padding:8px 20px;background:#4caf50;color:#fff;border:none;cursor:pointer;}
  .safe{background:#1a3a1a;border:1px solid #4caf50;padding:12px;margin:10px 0;border-radius:5px;}
  .result{background:#333;padding:12px;margin:10px 0;}
  code{background:#222;padding:2px 6px;}
  a{color:#4caf50;}
</style></head>
<body>
  <h2>✅ Secure Login — Parameterized Query</h2>
  <div class="safe">
    🔒 This form uses <strong>parameterized queries</strong> (prepared statements).<br>
    SQL injection payloads are treated as literal text, not SQL code.<br>
    Demo credentials: <code>sachin</code> / <code>password1</code>
  </div>
  <form method="POST">
    <label>Username:</label><br>
    <input type="text" name="username" placeholder="sachin"><br>
    <label>Password:</label><br>
    <input type="password" name="password" placeholder="password1"><br><br>
    <button type="submit">Login</button>
  </form>
  {% if result %}
  <div class="result">{{ result }}</div>
  {% endif %}
  <br><a href="/">← Back</a> | <a href="/sqli/vulnerable">See Vulnerable Version →</a>
</body></html>
"""

@app.route("/sqli/secure", methods=["GET", "POST"])
def sqli_secure():
    """Demonstrate secure SQL query with parameterized queries."""
    result = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        try:
            # ✅ SECURE: Parameterized query — user input never touches SQL syntax
            conn = sqlite3.connect(DATABASE_FILE)
            cur = conn.cursor()
            
            # First, get the salt for the user
            cur.execute("SELECT salt FROM users WHERE username = ?", (username,))
            salt_row = cur.fetchone()
            
            if salt_row:
                salt = salt_row[0]
                # Hash the password with the stored salt
                hashed_pw = hashlib.sha256((salt + password).encode()).hexdigest()
                
                # Now verify password
                cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
                user = cur.fetchone()
                conn.close()
                
                if user:
                    result = f"✅ Welcome, {user[1]}! (Role: {user[4]})"
                else:
                    result = "❌ Invalid credentials."
            else:
                conn.close()
                result = "❌ Invalid credentials."
                
        except Exception as e:
            result = f"[DB ERROR] {str(e)[:100]}"

    return render_template_string(SQLI_SECURE_HTML, result=result)


# ─────────────────────────────────────────
#  2. XSS — VULNERABLE
# ─────────────────────────────────────────
XSS_VULN_HTML = """
<!DOCTYPE html><html>
<head><title>Vulnerable Comments (XSS)</title>
<style>
  body{font-family:monospace;background:#1a0a0a;color:#eee;padding:30px;}
  input,textarea{padding:8px;margin:5px;width:350px;background:#333;color:#fff;border:1px solid #e94560;}
  button{padding:8px 20px;background:#e94560;color:#fff;border:none;cursor:pointer;}
  .vuln{background:#3a1a1a;border:1px solid #e94560;padding:12px;margin:10px 0;border-radius:5px;}
  .comment{background:#2a2a2a;padding:10px;margin:5px 0;border-left:3px solid #e94560;}
  a{color:#e94560;}
</style></head>
<body>
  <h2>❌ Vulnerable Comment Box — XSS Demo</h2>
  <div class="vuln">
    ⚠️ Comments are rendered as raw HTML — XSS is possible!<br>
    Try payload: <code>&lt;script&gt;alert('XSS by Sachin!')&lt;/script&gt;</code>
  </div>
  <form method="POST">
    <label>Your name:</label><br>
    <input type="text" name="user" value="Sachin"><br>
    <label>Comment (try injecting script):</label><br>
    <textarea name="comment" rows="3">&lt;script&gt;alert('XSS!')&lt;/script&gt;</textarea><br><br>
    <button type="submit">Post Comment</button>
  </form>
  <h3>Comments:</h3>
  {% for c in comments %}
  <div class="comment">
    <strong>{{ c[1] | safe }}:</strong> {{ c[2] | safe }}
  </div>
  {% endfor %}
  <br><a href="/">← Back</a> | <a href="/xss/secure">See Secure Version →</a>
</body></html>
"""

comments_vulnerable = []   # In-memory store for demo

@app.route("/xss/vulnerable", methods=["GET", "POST"])
def xss_vulnerable():
    """Demonstrate XSS vulnerability."""
    if request.method == "POST":
        user = request.form.get("user", "Anonymous")
        comment = request.form.get("comment", "")
        # ❌ VULNERABLE: Storing raw input and rendering with | safe (no encoding)
        comments_vulnerable.append((None, user, comment))
    return render_template_string(XSS_VULN_HTML, comments=comments_vulnerable)


# ─────────────────────────────────────────
#  2. XSS — SECURE
# ─────────────────────────────────────────
XSS_SECURE_HTML = """
<!DOCTYPE html><html>
<head><title>Secure Comments</title>
<style>
  body{font-family:monospace;background:#0a1a0a;color:#eee;padding:30px;}
  input,textarea{padding:8px;margin:5px;width:350px;background:#333;color:#fff;border:1px solid #4caf50;}
  button{padding:8px 20px;background:#4caf50;color:#fff;border:none;cursor:pointer;}
  .safe{background:#1a3a1a;border:1px solid #4caf50;padding:12px;margin:10px 0;border-radius:5px;}
  .comment{background:#2a2a2a;padding:10px;margin:5px 0;border-left:3px solid #4caf50;}
  a{color:#4caf50;}
</style></head>
<body>
  <h2>✅ Secure Comment Box — Output Encoding</h2>
  <div class="safe">
    🔒 All user input is <strong>HTML-encoded</strong> before rendering.<br>
    Script tags become plain text — no XSS possible!
  </div>
  <form method="POST">
    <label>Your name:</label><br>
    <input type="text" name="user" value="Sachin"><br>
    <label>Comment (try the same payload):</label><br>
    <textarea name="comment" rows="3">&lt;script&gt;alert('XSS!')&lt;/script&gt;</textarea><br><br>
    <button type="submit">Post Comment</button>
  </form>
  <h3>Comments:</h3>
  {% for c in comments %}
  <div class="comment">
    <strong>{{ c[0] }}:</strong> {{ c[1] }}
  </div>
  {% endfor %}
  <br><a href="/">← Back</a> | <a href="/xss/vulnerable">See Vulnerable Version →</a>
</body></html>
"""

comments_secure = []

@app.route("/xss/secure", methods=["GET", "POST"])
def xss_secure():
    """Demonstrate secure XSS prevention with output encoding."""
    if request.method == "POST":
        user    = request.form.get("user", "Anonymous")
        comment = request.form.get("comment", "")
        # ✅ SECURE: html.escape() encodes all special characters
        safe_user    = html.escape(user)
        safe_comment = html.escape(comment)
        comments_secure.append((safe_user, safe_comment))
    return render_template_string(XSS_SECURE_HTML, comments=comments_secure)


# ─────────────────────────────────────────
#  3. IDOR — VULNERABLE
# ─────────────────────────────────────────
IDOR_VULN_HTML = """
<!DOCTYPE html><html>
<head><title>Vulnerable Profile (IDOR)</title>
<style>
  body{font-family:monospace;background:#1a0a0a;color:#eee;padding:30px;}
  .vuln{background:#3a1a1a;border:1px solid #e94560;padding:12px;margin:10px 0;border-radius:5px;}
  .profile{background:#2a2a2a;padding:15px;margin:10px 0;}
  a{color:#e94560;}
</style></head>
<body>
  <h2>❌ Vulnerable Profile — IDOR Demo</h2>
  <div class="vuln">
    ⚠️ No authorization check! Any user can view any profile.<br>
    Change the <code>?id=</code> parameter in the URL to see other users.
  </div>
  {% if user %}
  <div class="profile">
    <p><strong>ID:</strong> {{ user[0] }}</p>
    <p><strong>Username:</strong> {{ user[1] }}</p>
    <p><strong>Password Hash:</strong> {{ user[2][:32] }}...</p>
    <p><strong>Role:</strong> {{ user[4] }}</p>
  </div>
  {% else %}
  <p>User not found.</p>
  {% endif %}
  <p>Try: <a href="/idor/vulnerable?id=1">id=1</a> | <a href="/idor/vulnerable?id=2">id=2</a> | <a href="/idor/vulnerable?id=3">id=3</a></p>
  <br><a href="/">← Back</a> | <a href="/idor/secure?id=1">See Secure Version →</a>
</body></html>
"""

@app.route("/idor/vulnerable")
def idor_vulnerable():
    """Demonstrate IDOR vulnerability."""
    try:
        user_id = request.args.get("id", 1, type=int)
    except (ValueError, TypeError):
        user_id = 1
    
    # ❌ VULNERABLE: No check if this user is allowed to see this profile
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cur.fetchone()
        conn.close()
    except Exception as e:
        user = None
    
    return render_template_string(IDOR_VULN_HTML, user=user)


# ─────────────────────────────────────────
#  3. IDOR — SECURE
# ─────────────────────────────────────────
IDOR_SECURE_HTML = """
<!DOCTYPE html><html>
<head><title>Secure Profile</title>
<style>
  body{font-family:monospace;background:#0a1a0a;color:#eee;padding:30px;}
  .safe{background:#1a3a1a;border:1px solid #4caf50;padding:12px;margin:10px 0;border-radius:5px;}
  .profile{background:#2a2a2a;padding:15px;margin:10px 0;}
  a{color:#4caf50;}
  .error{color:#e94560;}
</style></head>
<body>
  <h2>✅ Secure Profile — Authorization Check</h2>
  <div class="safe">
    🔒 Server checks: does the logged-in user own this profile?<br>
    You are logged in as: <strong>{{ current_user }}</strong> (id={{ current_id }})
  </div>
  {% if error %}
  <p class="error">⛔ {{ error }}</p>
  {% elif user %}
  <div class="profile">
    <p><strong>ID:</strong> {{ user[0] }}</p>
    <p><strong>Username:</strong> {{ user[1] }}</p>
    <p><strong>Role:</strong> {{ user[4] }}</p>
  </div>
  {% endif %}
  <p>Try: <a href="/idor/secure?id=1">id=1</a> | <a href="/idor/secure?id=2">id=2</a> | <a href="/idor/secure?id=3">id=3</a></p>
  <br><a href="/">← Back</a> | <a href="/idor/vulnerable?id=1">See Vulnerable Version →</a>
</body></html>
"""

@app.route("/idor/secure")
@login_required
def idor_secure():
    """Demonstrate secure access control with authorization checks."""
    try:
        requested_id = request.args.get("id", session.get('user_id'), type=int)
    except (ValueError, TypeError):
        requested_id = session.get('user_id')
    
    current_user_id = session.get('user_id')
    current_username = session.get('username')

    # ✅ SECURE: Check if requested profile belongs to the logged-in user
    if requested_id != current_user_id:
        error_msg = f"Access denied! You can only view your own profile (id={current_user_id})."
        return render_template_string(
            IDOR_SECURE_HTML,
            user=None,
            error=error_msg,
            current_user=current_username,
            current_id=current_user_id
        )

    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        cur.execute("SELECT id, username, password, salt, role FROM users WHERE id = ?", (requested_id,))
        user = cur.fetchone()
        conn.close()
    except Exception as e:
        user = None

    return render_template_string(
        IDOR_SECURE_HTML,
        user=user,
        error=None,
        current_user=current_username,
        current_id=current_user_id
    )


# ─────────────────────────────────────────
#  4. AUTHENTICATION FAILURES
# ─────────────────────────────────────────
AUTH_HTML = """
<!DOCTYPE html><html>
<head><title>Auth Comparison</title>
<style>
  body{font-family:monospace;background:#0a0a1a;color:#eee;padding:30px;}
  .box{display:inline-block;vertical-align:top;width:45%;margin:10px;padding:15px;
       background:#1a1a2e;border-radius:8px;}
  .vuln{border:2px solid #e94560;}
  .safe{border:2px solid #4caf50;}
  code{background:#333;padding:2px 5px;display:block;margin:5px 0;font-size:13px;word-break:break-all;}
  a{color:#aaa;}
</style></head>
<body>
  <h2>🔐 Authentication — Weak vs Strong Hashing</h2>
  <div class="box vuln">
    <h3 style="color:#e94560">❌ Weak (MD5)</h3>
    <p>MD5 is broken — fast to crack with rainbow tables.</p>
    <p>MD5('password1') =</p>
    <code>{{ md5_hash }}</code>
    <p>Crackable in seconds on sites like crackstation.net</p>
  </div>
  <div class="box safe">
    <h3 style="color:#4caf50">✅ Strong (SHA-256 + Random Salt)</h3>
    <p>Salted SHA-256 with random per-user salt — rainbow tables fail.</p>
    <p>Salt = {{ salt }}</p>
    <p>SHA-256(salt + 'password1') =</p>
    <code>{{ sha256_hash }}</code>
    <p>Each user has a unique salt, making rainbow tables useless.</p>
    <p><strong>Production Best Practice:</strong> Use bcrypt or argon2.</p>
  </div>
  <br><a href="/">← Back</a>
</body></html>
"""

@app.route("/auth/weak")
@app.route("/auth/strong")
def auth_comparison():
    """Compare weak vs strong password hashing."""
    password = "password1"
    salt = secrets.token_hex(16)  # ✅ Generate random salt

    md5_hash    = hashlib.md5(password.encode()).hexdigest()
    sha256_hash = hashlib.sha256((salt + password).encode()).hexdigest()

    return render_template_string(
        AUTH_HTML,
        md5_hash=md5_hash,
        sha256_hash=sha256_hash,
        salt=salt
    )


# ─────────────────────────────────────────
#  ERROR HANDLERS
# ─────────────────────────────────────────
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return f"""
    <!DOCTYPE html><html>
    <head><title>Not Found</title></head>
    <body style="font-family:monospace;background:#1a1a2e;color:#eee;padding:30px;">
      <h1>404 - Page Not Found</h1>
      <a href="/">← Back to Home</a>
    </body></html>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return f"""
    <!DOCTYPE html><html>
    <head><title>Server Error</title></head>
    <body style="font-family:monospace;background:#1a1a2e;color:#eee;padding:30px;">
      <h1>500 - Internal Server Error</h1>
      <p>An unexpected error occurred.</p>
      <a href="/">← Back to Home</a>
    </body></html>
    """, 500


# ─────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────
if __name__ == "__main__":
    # Initialize database
    init_db()
    
    print("=" * 60)
    print("  Web Security Demo — Sachin Kumar")
    print("  sachinyadav2063@gmail.com")
    print(f"  Open: http://{HOST}:{PORT}")
    print("  ⚠️  Run ONLY on localhost — educational use only")
    print("=" * 60)
    
    # Run the Flask app
    app.run(debug=DEBUG, host=HOST, port=PORT)
