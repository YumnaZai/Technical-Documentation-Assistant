# Project README

## What This Is

A multi-service platform consisting of `auth-service`, `user-service`,
`api-gateway`, and `web-client`. See `architecture/system_design.md` for
the full system design.

## Services

| Service       | Port  | Depends on     | Purpose                          |
|---------------|-------|----------------|-----------------------------------|
| auth-service  | 4001  | Postgres       | Login, JWT issuance, refresh tokens |
| user-service  | 4002  | Postgres       | User profiles, roles              |
| api-gateway   | 4000  | auth-service    | Routes requests, verifies JWTs    |
| web-client    | 3000  | api-gateway     | Frontend                          |

## Running Locally

```bash
git clone <this repo>
cd platform
docker-compose up
```

This starts all four services plus a local Postgres instance. The
`auth-service` must be healthy before `api-gateway` will accept traffic —
`docker-compose` handles this via a healthcheck dependency.

## Environment Variables

`auth-service` requires:
```
JWT_PRIVATE_KEY=       # RS256 private key, PEM format
JWT_ACCESS_TTL=900      # 15 minutes, in seconds
JWT_REFRESH_TTL=604800  # 7 days, in seconds
OAUTH_GOOGLE_CLIENT_ID=
OAUTH_GOOGLE_CLIENT_SECRET=
OAUTH_GITHUB_CLIENT_ID=
OAUTH_GITHUB_CLIENT_SECRET=
```

`api-gateway` requires:
```
JWT_PUBLIC_KEY=         # matching public key, PEM format
```

## Testing Login Locally

Once services are running, you can hit the login endpoint directly:
```bash
curl -X POST http://localhost:4001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```

For full endpoint documentation, see `api/auth.md` and `api/users.md`.

## First-Time Setup

New to the team? Start with `wiki/onboarding.txt` — it walks through
account access, local setup order, and the most common first-week
authentication debugging gotchas.

## Contributing

Standard PR flow — branch off `main`, open a PR, one approval required.
Changes to `auth-service` specifically require review from someone on
the platform-eng team due to the security-sensitive nature of the code.
