# ServiceSlot

Plain PHP backend and server-rendered frontend for technical-service bookings. Create requests, search clients/services, update appointment status and persist records in SQLite. PDO prepared statements, date validation, escaped HTML, session CSRF tokens, security headers and redirect-after-post.

## Run
PHP 8.3+ with `pdo_sqlite`:
```sh
php -S 127.0.0.1:8081 -t public
```
Open http://127.0.0.1:8081. The database is created outside `public/` in `data/`.
Syntax check: `php -l public/index.php`.

## Verify
Create a future booking, confirm it, search by client, restart and verify persistence. Submit a past date or missing CSRF token and verify rejection. Enter `<script>alert(1)</script>` as a client and verify it is displayed as plain text. No double-booking constraint is implied: this is a request queue, not a capacity scheduler. Local single-operator demo without login; add authentication, role checks and operational time-zone configuration before shared use.
