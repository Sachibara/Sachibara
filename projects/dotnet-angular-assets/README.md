# Asset Lifecycle Console

.NET 10 ASP.NET Core Minimal API + Angular 20 / TypeScript + EF Core SQLite. Create, list, edit and delete equipment; unique normalized asset tags; lifecycle states; owner search; persistent database; error and loading states.

## Run
Install .NET 10 SDK and Node 22.18+.
Terminal 1, from `api/`:
```sh
dotnet restore
dotnet run --urls http://127.0.0.1:5080
```
Terminal 2, from `web/`:
```sh
npm install
npm run dev
```
Open http://localhost:4200. The Angular dev proxy forwards `/api` to .NET. `npm run build` checks Angular templates and compiles the frontend; `dotnet build` compiles the API. API data is in `api/data/assets.db`.

## Verify
From `projects/`, with the API running: `python tests/api_smoke.py assets http://127.0.0.1:5080`.
Demonstrate duplicate rejection, Assigned → Repair transition, owner filtering, and records surviving an API restart.

## Scope
Single-operator local demo, without authentication. Bind to loopback as shown. Deployment needs authentication/authorization, an EF migration strategy instead of EnsureCreated, and a reverse proxy serving Angular with `/api` routed to the API. Static hosting alone cannot run .NET or store SQLite.
