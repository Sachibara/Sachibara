# ChangeGate API

Ruby / Sinatra backend for infrastructure change requests. Bearer authentication, SQLite persistence, request validation, bounded payloads and compare-and-set workflow updates. Draft → Approved → Implemented; Draft → Rejected. Invalid transitions return 409.

## Run
Ruby 3.3+, Bundler:
```sh
bundle install
```
Set `CHANGE_API_TOKEN` to a randomly generated secret of at least 32 characters. PowerShell example:
```powershell
$env:CHANGE_API_TOKEN = [guid]::NewGuid().ToString() + [guid]::NewGuid().ToString()
bundle exec ruby app.rb
```
On bash, export the variable before the same Ruby command. API: http://127.0.0.1:4567.
```sh
curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:4567/changes
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" -d '{"title":"Replace branch switch","risk":"High"}' http://127.0.0.1:4567/changes
```
PATCH `/changes/1/status` with `{"status":"Approved"}`, then `Implemented`. `bundle exec ruby tests/api_test.rb` verifies authentication, validation and transitions. GET list is limited to the newest 500 requests.

This is a backend project without a frontend. A shared operator token is appropriate for the local demo; production needs individual identities, approval-role separation, audit history, TLS and pagination. SQLite defaults to `data/changes.sqlite`; `CHANGE_DB_PATH` can override it.
