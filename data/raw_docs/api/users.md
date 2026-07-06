# Users API

## Overview

Endpoints for creating, reading, updating, and deleting user accounts.
Most endpoints in this file require authentication — see `api/auth.md`
for how to obtain an access token.

## Create User

`POST /users` creates a new account directly (used by admin tools and
internal scripts). Regular signups go through `POST /auth/login` with a
`create_if_missing` flag or through OAuth, which creates the user record
automatically as part of the authentication flow.

```
POST /users
Authorization: Bearer <admin access token>
{
  "email": "new.user@example.com",
  "role": "member"
}
```

## Get Current User

`GET /users/me` returns the profile of the currently authenticated user.
This endpoint requires a valid access token in the `Authorization` header
— it is the simplest way to check whether a token is still valid, since it
returns `401` immediately if the JWT has expired or failed signature
verification.

## Update User

`PATCH /users/{id}` updates profile fields. Users may only update their own
record unless they hold the `admin` role. Role changes themselves require
`admin` and are logged in the audit table.

## Delete User

`DELETE /users/{id}` soft-deletes the account and immediately revokes all
of that user's refresh tokens (see `api/auth.md` for how refresh token
revocation works), forcing any active sessions to re-authenticate and then
fail since the account no longer exists.

## Roles and Permissions

| Role    | Can view own profile | Can view others | Can change roles |
|---------|----------------------|------------------|-------------------|
| member  | Yes                   | No               | No                |
| admin   | Yes                   | Yes              | Yes               |

Role information is embedded as a claim inside the JWT access token issued
during authentication, so permission checks on these endpoints don't
require a database lookup on every request.
