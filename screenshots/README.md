# Screenshots

This folder contains screenshots of the Web Security Learning Project in action.

## Project Screenshots

### 1. Login Page
The main login interface where users authenticate with their credentials.
- Simple and clean login form
- Username and password fields
- Login button

### 2. Dashboard Page
The user dashboard displayed after successful authentication.
- Personalized greeting with username
- User profile information
- Security headers visible in browser dev tools
- Session management active

### 3. Profile Page
Individual user profile page showing user-specific data.
- User ID and username display
- Secure per-user salt implementation
- IDOR vulnerability demonstration (safely contained)
- User information retrieval

### 4. Security Headers
Browser developer tools showing security headers implemented:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security
- Content-Security-Policy

### 5. Network Tab
Network requests showing:
- HTTP 200 responses for authenticated requests
- 401 Unauthorized for unauthenticated requests
- 404 for non-existent routes
- Security headers in response

### 6. Browser Console
Console output showing:
- No security errors
- Successful authentication logs
- Clean error handling

### 7. Error Handling
Error pages demonstrating:
- Custom 404 Page Not Found
- Custom 500 Server Error
- User-friendly error messages

## How to Generate Screenshots

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open browser to `http://127.0.0.1:5000`

3. Use credentials:
   - Username: `sachin`
   - Password: `password1`

4. Navigate through different pages and take screenshots using:
   - Browser built-in screenshot tool (Ctrl+Shift+S on Chrome)
   - Developer tools (F12)
   - Third-party screenshot tools

## Security Learning Points

Each screenshot demonstrates important web security concepts:
- **Authentication**: Proper login mechanisms
- **Session Management**: Secure session handling
- **Input Validation**: Protection against malicious input
- **Security Headers**: Defense against common attacks
- **Error Handling**: Graceful error management
- **HTTPS Best Practices**: Security in transit

