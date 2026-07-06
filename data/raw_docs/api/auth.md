# Authentication API

## Overview

The platform uses JWT-based authentication with a short-lived access token
and a longer-lived refresh token. All authenticated endpoints require a
valid access token passed in the `Authorization` header.

## Login Flow

1. Client submits credentials to `POST /auth/login`
2. Server validates the email/password against the `users` table
3. On success, server issues:
   - An **access token** (JWT, 15 minute expiry)
   - A **refresh token** (opaque string, 7 day expiry, stored in the `refresh_tokens` table)
4. Client stores the access token in memory and the refresh token in an
   HttpOnly cookie

```
POST /auth/login
{
  "email": "user@example.com",
  "password": "••••••••"
}

Response 200
{
  "access_token": "eyJhbGciOi...",
  "refresh_token": "rt_9f8a7b...",
  "expires_in": 900
}
```

## Token Refresh

When the access token expires, the client calls `POST /auth/refresh` with
the refresh token to obtain a new access token without forcing the user to
log in again.

```
POST /auth/refresh
{
  "refresh_token": "rt_9f8a7b..."
}
```

If the refresh token is expired or revoked, this endpoint returns `401` and
the client must redirect to login.

## OAuth Integration

The platform supports third-party login via `GET /auth/oauth/{provider}`,
currently configured for `google` and `github`. OAuth logins create or
link a row in the `users` table and issue the same access/refresh token
pair as a normal login.

## Logout

`POST /auth/logout` revokes the current refresh token server-side. Access
tokens are not revocable individually since they are stateless JWTs — this
is why the access token expiry is kept short (15 minutes).

## Password Reset

`POST /auth/password-reset/request` sends a one-time reset link valid for
30 minutes. `POST /auth/password-reset/confirm` accepts the reset token and
a new password.

## Related Docs

- See `architecture/system_design.md` for how JWTs are signed and verified
  across services.
- See `readmes/project.md` for how to run the auth service locally.
