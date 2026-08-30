
## Authentication security

Authentication uses short-lived JWT access tokens plus server-side refresh sessions.

- Access tokens expire according to `ACCESS_TOKEN_EXPIRE_MINUTES`.
- Refresh tokens expire according to `REFRESH_TOKEN_EXPIRE_DAYS` (default: 7 days).
- Refresh tokens are opaque, stored only as SHA-256 hashes in `auth_sessions`, and delivered in an HttpOnly cookie.
- Refresh tokens are rotated on every `/auth/refresh` request; the previous refresh token is invalid immediately.
- Every access token has a unique `jti` tied to an active database session. Protected endpoints check that session, so logout/revocation invalidates the access token immediately.
- `/auth/logout` revokes the current refresh session and clears the refresh cookie.
- Set `REFRESH_COOKIE_SECURE=true` in HTTPS production deployments.
- `REFRESH_COOKIE_SAMESITE` defaults to `lax`.

Required new environment settings are optional because safe defaults are provided:

```env
REFRESH_TOKEN_EXPIRE_DAYS=7
REFRESH_COOKIE_NAME=mobile_shop_refresh_token
REFRESH_COOKIE_SECURE=false
REFRESH_COOKIE_SAMESITE=lax
```

After updating the backend, apply the migration:

```bash
alembic upgrade head
```
