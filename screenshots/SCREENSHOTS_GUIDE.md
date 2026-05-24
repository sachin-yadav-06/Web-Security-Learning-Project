# Web Security Learning Project - Screenshots & Documentation

## 📸 Project Screenshots

This folder contains visual documentation of the Web Security Learning Project in action, demonstrating various security concepts and features.

---

## 🖼️ Screenshot Guide

### 1. **Login Page** (`01_login.png`)
```
Shows:
✅ Secure login interface
✅ Username field
✅ Password field  
✅ Login button
✅ Demo credentials displayed
✅ Error message handling
```

**Security Features Visible:**
- Session cookie creation
- HTTPS ready (in production)
- Secure authentication flow

---

### 2. **Dashboard/Home Page** (`02_dashboard.png`)
```
Shows:
✅ User welcome message with username
✅ User role display
✅ Navigation to vulnerability demos
✅ Logout button
✅ Warning about educational use
```

**Security Features:**
- Session validation
- User role management
- Secure navigation

---

### 3. **SQL Injection - Vulnerable Demo** (`03_sqli_vulnerable.png`)
```
Shows:
❌ VULNERABLE SQL query execution
❌ Direct string concatenation
❌ Attack payload: ' OR '1'='1' --
❌ Successful SQL injection
```

**Educational Purpose:**
- Demonstrates SQL injection risk
- Shows how queries are constructed
- Proves need for parameterized queries

---

### 4. **SQL Injection - Secure Demo** (`04_sqli_secure.png`)
```
Shows:
✅ SECURE parameterized query
✅ Prepared statements with placeholders
✅ Safe input handling
✅ Attack payload blocked as literal text
```

**Security Features:**
- Parameterized queries (?)
- Input treated as data, not code
- Complete injection prevention

---

### 5. **XSS - Vulnerable Demo** (`05_xss_vulnerable.png`)
```
Shows:
❌ VULNERABLE XSS injection
❌ Raw HTML rendering
❌ JavaScript execution possible
❌ Comments rendered without encoding
```

**Educational Purpose:**
- Demonstrates XSS vulnerability
- Shows script tag injection
- Proves need for output encoding

---

### 6. **XSS - Secure Demo** (`06_xss_secure.png`)
```
Shows:
✅ SECURE HTML encoding
✅ html.escape() in action
✅ Script tags rendered as text
✅ Safe comment rendering
```

**Security Features:**
- Output encoding (html.escape)
- XSS injection blocked
- Safe rendering of user input

---

### 7. **IDOR - Vulnerable Demo** (`07_idor_vulnerable.png`)
```
Shows:
❌ VULNERABLE access control
❌ No authorization check
❌ User can view any profile by ID
❌ Access to other users' data
```

**Educational Purpose:**
- Demonstrates broken access control
- Shows IDOR vulnerability
- Proves need for authorization checks

---

### 8. **IDOR - Secure Demo** (`08_idor_secure.png`)
```
Shows:
✅ SECURE authorization check
✅ Access denied message
✅ User can only view own profile
✅ Server-side validation
```

**Security Features:**
- Session-based ownership verification
- Authorization check on each request
- Graceful error handling

---

### 9. **Authentication Comparison** (`09_auth_comparison.png`)
```
Shows:
❌ Weak MD5 hashing (crackable)
✅ Strong SHA-256 + Salt hashing (secure)
✅ Per-user random salt displayed
```

**Security Features:**
- Weak vs. strong hashing comparison
- Salt demonstration
- Production recommendations (bcrypt/argon2)

---

### 10. **Browser Security Headers** (`10_security_headers.png`)
```
Shows (F12 Developer Tools):
✅ Content-Security-Policy
✅ X-Frame-Options: DENY
✅ X-Content-Type-Options: nosniff
✅ Strict-Transport-Security
✅ Referrer-Policy: no-referrer
✅ Permissions-Policy
✅ X-XSS-Protection
```

**Security Features:**
- OWASP recommended headers
- Browser security enforcement
- Defense against common attacks

---

### 11. **Error Pages** (`11_error_404.png`, `12_error_500.png`)
```
Shows:
✅ Custom 404 Not Found page
✅ Custom 500 Server Error page
✅ Secure error messages
✅ No sensitive information leaked
```

**Security Features:**
- Graceful error handling
- No stack traces exposed
- User-friendly messages

---

### 12. **Database Schema** (`13_database_schema.png`)
```
Shows:
📊 Users table structure:
   - id (PRIMARY KEY)
   - username (UNIQUE)
   - password (hashed with salt)
   - salt (per-user random salt)
   - role (user/admin)

📊 Comments table structure:
   - id (PRIMARY KEY)
   - user (commenter)
   - comment (XSS demo)
```

---

### 13. **Source Code Comparison** (`14_code_comparison.png`)
```
Shows:
❌ Vulnerable code patterns
✅ Secure code patterns
📝 Side-by-side comparison
```

---

## 📋 How to Generate These Screenshots

### 1. Start the Application
```bash
pip install -r requirements.txt
python app.py
```

### 2. Access the Application
Open browser: `http://127.0.0.1:5000`

### 3. Login
Use credentials:
```
Username: sachin
Password: password1
```

### 4. Take Screenshots

#### Using Chrome DevTools:
- Press `Ctrl + Shift + S` (or `Cmd + Shift + S` on Mac)
- Select area to capture
- Screenshot automatically downloaded

#### Using Browser Built-in:
1. Press `F12` to open Developer Tools
2. Press `Ctrl + Shift + P` (Command Palette)
3. Type "screenshot" → "Capture full page screenshot"

#### Using Third-Party Tools:
- Snagit
- Greenshot
- ShareX
- PicPick

### 5. Navigate Pages
- Click through each vulnerability demo
- Open DevTools (F12) to show security headers
- Navigate to Network tab to show requests
- Navigate to Console tab to show logs

---

## 🔍 What Each Screenshot Demonstrates

| Screenshot | Key Learning | Vulnerability Category |
|-----------|--------------|----------------------|
| 01-02 | Authentication & Session Management | A07 - Auth Failures |
| 03-04 | SQL Injection Prevention | A03 - Injection |
| 05-06 | XSS Prevention | A03 - Injection |
| 07-08 | Access Control | A01 - Broken Access Control |
| 09 | Cryptographic Failures | A02 - Crypto Failures |
| 10 | Security Misconfiguration | A05 - Security Misconfig |
| 11-12 | Error Handling | A01 - Information Disclosure |
| 13 | Database Security | A01 - Injection |

---

## 📚 Security Concepts Demonstrated

### Input Validation
- Parameterized queries
- Output encoding
- Type validation

### Output Encoding
- HTML escaping
- Safe rendering
- Script prevention

### Authorization
- Session checks
- User ownership verification
- Role-based access control

### Cryptography
- Proper hashing (SHA-256 + salt)
- Per-user salt generation
- Bcrypt/Argon2 recommendations

### Security Headers
- Content-Security-Policy
- X-Frame-Options
- HSTS
- X-Content-Type-Options

### Error Handling
- Custom error pages
- No information leakage
- User-friendly messages

---

## 🎯 Educational Uses

These screenshots can be used for:
- **Classroom Teaching** - Show real vulnerabilities
- **Documentation** - Visual reference guide
- **Presentations** - Demonstrate security concepts
- **Portfolio** - Show security learning projects
- **Blog Posts** - Illustrate security articles

---

## 📖 OWASP Mapping

| OWASP # | Vulnerability | Screenshot |
|---------|----------------|-----------|
| A01 | Broken Access Control | 07, 08 |
| A02 | Cryptographic Failures | 09 |
| A03 | Injection (SQLi, XSS) | 03, 04, 05, 06 |
| A05 | Security Misconfiguration | 10 |
| A07 | Auth & Session Failures | 01, 02 |

---

## ✅ Screenshot Checklist

To create a complete screenshot set:

- [ ] Login page (successful & failed)
- [ ] Dashboard/home page
- [ ] SQLi vulnerable endpoint
- [ ] SQLi secure endpoint
- [ ] XSS vulnerable endpoint
- [ ] XSS secure endpoint
- [ ] IDOR vulnerable endpoint
- [ ] IDOR secure endpoint
- [ ] Auth comparison page
- [ ] Browser security headers (DevTools)
- [ ] 404 error page
- [ ] 500 error page
- [ ] Source code examples
- [ ] Database schema
- [ ] Network tab (requests)
- [ ] Console tab (no errors)

---

## 🎬 Video Recording Alternative

Instead of static screenshots, you could also:
1. Record a demo video showing the app
2. Show vulnerable vs. secure endpoints
3. Demonstrate browser DevTools
4. Explain security concepts
5. Upload to YouTube or project documentation

---

## 📝 Notes

- Screenshots are for educational purposes only
- Vulnerability demonstrations are contained and safe
- No real systems are compromised
- All demos run on localhost (127.0.0.1:5000)
- Ethical hacking demonstration only

---

**Happy Learning! 🛡️**

Author: Sachin Kumar  
Email: sachinyadav2063@gmail.com  
GitHub: https://github.com/sachin-yadav-06
