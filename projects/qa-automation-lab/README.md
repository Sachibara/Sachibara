# QA Automation Lab

Playwright + TypeScript tests exercise the actual Ops Studio browser → HTTP API → SQLite → rendered response flow. They cover subnet planning, invalid capacity, secret redaction, security findings, endpoint checks, idempotent imports, knowledge citations, real service probing and mobile layout. Test data uses an isolated temporary database.

## Run
Python 3.11+ and Node 22+:
```sh
npm install
npx playwright install chromium
npm test
```
The configuration starts/stops its own Ops Studio server on 8097. Do not start another server on that port. Open the HTML report with `npm run report`. Browser failures retain a screenshot and trace. Dependencies/browser binaries must be installed first; traces may contain test inputs.

The Node API project has separate actual HTTP authorization/concurrency tests. This suite does not certify the native mobile application or third-party platforms.
