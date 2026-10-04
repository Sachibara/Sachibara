# Operations Platform

React + TypeScript client and Node.js API with real accounts, scrypt password hashing, hashed expiring sessions, per-owner incident access, administrator visibility/audit, validation and optimistic concurrency. Incident mutations and audit events commit atomically. SQLite is a download-free local mode; `DATABASE_URL` switches the same repository interface to PostgreSQL using `pg`.

## Local run
Node 24 is required for native `node:sqlite`.
```sh
npm start
```
The API listens on http://127.0.0.1:5081 and prints the initial administrator email and a generated password on the first run. Store that password. Set `ADMIN_EMAIL` and `ADMIN_PASSWORD` before first run to use your own credentials; changing them does not reset an existing account. Other users register as operators.

In another terminal:
```sh
cd web
npm install
npm run dev
```
Open the Vite URL. The client proxies `/api` to port 5081. `npm run build` checks TypeScript and produces frontend assets. The API root is an informational page, not the React application.

## PostgreSQL
Run `npm install` in the project root, configure `DATABASE_URL` with your database connection string, then start. The startup schema creates missing tables; existing schema evolution needs migrations before a production release. `../delivery-cloud-lab/compose.yaml` provides a PostgreSQL + API + frontend setup. SQLite data is in `data/operations.sqlite`.

## Tests
`npm test` runs the actual HTTP API against disposable SQLite: accounts, duplicate emails, isolation, administrator authorization, stale updates/deletes, audit and logout. PostgreSQL and frontend builds require dependency installation and are not verified by that test.

Sessions last 12 hours. The browser keeps a bearer token in sessionStorage; mobile uses SecureStore. Local development uses HTTP; shared use requires TLS. No password recovery, email verification or production-grade registration/rate-limit service is implemented. List endpoints cap results at 500 incidents and 200 audit events. There are no seeded incident records or fake cloud connections.
