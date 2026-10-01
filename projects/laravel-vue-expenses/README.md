# Expense Atlas

Laravel 12 / PHP + Vue 3 (VueJS) fullstack spending tracker. CRUD, category filtering, totals in Philippine pesos, integer centavo storage, input validation, CSRF-protected web routes, database migration, and a feature test.

## Run
PHP 8.3+, Composer, Python 3, Node 22.18+, SQLite PHP extension:
```sh
python setup.py
cd runtime
npm install
npm run build
php artisan serve --host=127.0.0.1 --port=8000
```
Visit http://127.0.0.1:8000. For frontend hot reload, use `npm run dev` in another terminal. `php artisan test --filter=ExpenseTest` exercises CRUD and invalid input. SQLite data lives in `runtime/database/database.sqlite`.

`overlay/` contains the complete project-specific implementation. `setup.py` downloads the official Laravel shell at the selected 12.x major, overlays these files, configures SQLite and migrates. It refuses to overwrite an existing runtime. Dependency lockfiles are generated during setup; commit them in a standalone deployment repository for reproducible releases.

## Showcase
Create Travel and Equipment expenses, filter totals, edit amount and refresh. Demonstrate rejection of negative amounts. Laravel escapes via Vue interpolation and uses web middleware CSRF. This local single-ledger demo has no user accounts; production requires authentication and per-user authorization. Do not expose the development server publicly.
