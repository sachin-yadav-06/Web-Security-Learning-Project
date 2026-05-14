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

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)   # Secure session key

# ─────────────────────────────────────────
#  DATABASE SETUP (In-memory SQLite)
# ─────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("demo.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role     TEXT DEFAULT 'user'
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user    TEXT,
            comment TEXT
        )
    """)
    # Seed demo users
    cur.execute("DELETE FROM users")
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ("admin", hashlib.sha256("admin123".encode()).hexdigest(), "admin"))
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ("sachin", hashlib.sha256("password1".encode()).hexdigest(), "user"))
    conn.commit()
    conn.close()


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
  </style>
</head>
<body>
  <h1>🛡️ Web Security Learning Demo</h1>
  <p>Author: <strong>Sachin Kumar</strong> | sachinyadav2063@gmail.com</p>

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
    🔗 GitHub: github.com/sachin | 📧 sachinyadav2063@gmail.com<br>
    Educational Project — OWASP Top 10 Demo
  </p>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HOME_HTML)


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
    result = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # ❌ VULNERABLE: Direct string concatenation — DO NOT DO THIS
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        try:
            conn = sqlite3.connect("demo.db")
            cur = conn.cursor()
            cur.execute(query)    # Dangerous! User input goes straight into query
            user = cur.fetchone()
            conn.close()

            if user:
                result = f"✅ Logged in as: {user[1]} (Role: {user[3]}) — SQLi succeeded!"
            else:
                result = "❌ Login failed."
        except Exception as e:
            result = f"[DB ERROR] {e} — (Hint: your injection may have broken the syntax)"

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
    result = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        # ✅ SECURE: Parameterized query — user input never touches SQL syntax
        query = "SELECT * FROM users WHERE username = ? AND password = ?"

        try:
            conn = sqlite3.connect("demo.db")
            cur = conn.cursor()
            cur.execute(query, (username, hashed_pw))   # Safe!
            user = cur.fetchone()
            conn.close()

            if user:
                result = f"✅ Welcome, {user[1]}! (Role: {user[3]})"
            else:
                result = "❌ Invalid credentials."
        except Exception as e:
            result = f"[DB ERROR] {e}"

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
    <p><strong>Password Hash:</strong> {{ user[2] }}</p>
    <p><strong>Role:</strong> {{ user[3] }}</p>
  </div>
  {% else %}
  <p>User not found.</p>
  {% endif %}
  <p>Try: <a href="/idor/vulnerable?id=1">id=1</a> | <a href="/idor/vulnerable?id=2">id=2</a></p>
  <br><a href="/">← Back</a> | <a href="/idor/secure?id=1">See Secure Version →</a>
</body></html>
"""


@app.route("/idor/vulnerable")
def idor_vulnerable():
    user_id = request.args.get("id", 1)
    # ❌ VULNERABLE: No check if this user is allowed to see this profile
    conn = sqlite3.connect("demo.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
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
</style></head>
<body>
  <h2>✅ Secure Profile — Authorization Check</h2>
  <div class="safe">
    🔒 Server checks: does the logged-in user own this profile?<br>
    In this demo, session user = 'sachin' (id=2). Trying id=1 is blocked.
  </div>
  {% if error %}
  <p style="color:#e94560;">⛔ {{ error }}</p>
  {% elif user %}
  <div class="profile">
    <p><strong>ID:</strong> {{ user[0] }}</p>
    <p><strong>Username:</strong> {{ user[1] }}</p>
    <p><strong>Role:</strong> {{ user[3] }}</p>
  </div>
  {% endif %}
  <p>Try: <a href="/idor/secure?id=1">id=1 (blocked)</a> | <a href="/idor/secure?id=2">id=2 (allowed)</a></p>
  <br><a href="/">← Back</a> | <a href="/idor/vulnerable?id=1">See Vulnerable Version →</a>
</body></html>
"""


@app.route("/idor/secure")
def idor_secure():
    # Simulate logged-in user is sachin (id=2)
    session["user_id"] = 2
    session["username"] = "sachin"

    requested_id = int(request.args.get("id", 2))

    # ✅ SECURE: Check if requested profile belongs to the logged-in user
    if requested_id != session["user_id"]:
        return render_template_string(
            IDOR_SECURE_HTML,
            user=None,
            error=f"Access denied! You can only view your own profile (id={session['user_id']})."
        )

    conn = sqlite3.connect("demo.db")
    cur = conn.cursor()
    cur.execute("SELECT id, username, password, role FROM users WHERE id = ?", (requested_id,))
    user = cur.fetchone()
    conn.close()
    return render_template_string(IDOR_SECURE_HTML, user=user, error=None)


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
  code{background:#333;padding:2px 5px;display:block;margin:5px 0;font-size:13px;}
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
    <h3 style="color:#4caf50">✅ Strong (SHA-256 + Salt)</h3>
    <p>Salted SHA-256 — unique per user, rainbow tables fail.</p>
    <p>SHA-256(salt + 'password1') =</p>
    <code>{{ sha256_hash }}</code>
    <p>Best practice: use bcrypt or argon2 in production.</p>
  </div>
  <br><a href="/">← Back</a>
</body></html>
"""


@app.route("/auth/weak")
@app.route("/auth/strong")
def auth_comparison():
    import hashlib
    password = "password1"
    salt = "sachin_random_salt_9x2k"

    md5_hash    = hashlib.md5(password.encode()).hexdigest()
    sha256_hash = hashlib.sha256((salt + password).encode()).hexdigest()

    return render_template_string(AUTH_HTML, md5_hash=md5_hash, sha256_hash=sha256_hash)


# ─────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("=" * 55)
    print("  Web Security Demo — Sachin Kumar")
    print("  sachinyadav2063@gmail.com")
    print("  Open: http://127.0.0.1:5000")
    print("  ⚠️  Run ONLY on localhost — educational use only")
    print("=" * 55)
    app.run(debug=True, host="127.0.0.1", port=5000)
