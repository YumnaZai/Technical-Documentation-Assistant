# System Design

## High-Level Architecture

The platform is split into four services:

- **auth-service** — issues and validates JWTs, manages refresh tokens
- **user-service** — owns the `users` table, profile data, roles
- **api-gateway** — routes incoming requests, verifies JWT signatures
  before forwarding to downstream services
- **web-client** — the frontend, talks to the gateway only

## Authentication Flow (System-Level View)

Unlike a typical single-service setup, JWT verification happens at the
**api-gateway** layer, not inside every individual service. This means:

1. `auth-service` is the only service that holds the private signing key
2. All access tokens are signed with RS256 (asymmetric signing)
3. `api-gateway` holds only the **public** key and verifies signatures
   locally, without calling `auth-service` on every request
4. Downstream services (user-service, etc.) trust the gateway and read
   the decoded JWT claims from request headers the gateway injects

This design avoids making `auth-service` a bottleneck — verifying a JWT
signature is a local cryptographic operation, not a network call.

## Why Refresh Tokens Are Opaque, Not JWTs

Refresh tokens are deliberately **not** JWTs. They are random opaque
strings stored in the `refresh_tokens` table in `auth-service`'s database.
This lets us revoke a specific refresh token immediately (e.g., on
logout or account deletion — see `api/users.md`) without needing a
token blocklist, which a stateless JWT refresh token would require.

## Data Storage

- `auth-service`: Postgres table `refresh_tokens` (token hash, user_id,
  expiry, revoked flag)
- `user-service`: Postgres table `users` (id, email, password_hash, role,
  created_at)
- Session state is never stored server-side beyond the refresh token —
  access tokens are fully stateless.

## Scaling Considerations

Because JWT verification is local to the gateway (public key only), the
gateway can be horizontally scaled without any shared session store. The
only stateful piece of the auth system is the refresh token table, which
sees far lower traffic than access-token verification.

## Related Docs

- `api/auth.md` — the actual login/refresh/logout endpoints
- `api/users.md` — how role claims are used for permission checks
- `wiki/onboarding.md` — new engineer setup, including local auth setup
