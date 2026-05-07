# 🍪 Cookie Security

## Overview

Cookies are small pieces of data used to maintain session state between clients and servers.

---

## Security Risks

Improperly handled cookies may expose:

- Session identifiers
- Authentication tokens
- User tracking information

---

## Recommended Protections

### Secure Flag

Ensures cookies are sent only over HTTPS.

---

### HttpOnly Flag

Prevents JavaScript access to cookies.

---

### SameSite Attribute

Helps mitigate CSRF attacks.

---

## Key Insight

Sensitive session data should never be transmitted through URL query parameters.
