# Ops Studio

A working local operations application with eight tools, a responsive browser interface, bearer-token access, SQLite persistence, validated imports and JSON exports. Python's standard library runs the whole app without package downloads. A FastAPI adapter exposes the same service layer when dependencies are installed.

## Run now
Python 3.11+:
```sh
python server.py
```
Open http://127.0.0.1:8090 and paste the operator token printed in the terminal. Choose a tool, Load example, then Run analysis. Press Ctrl+C to stop. The token changes on restart unless `OPS_TOKEN` is set. Data persists in `data/ops.sqlite`; back up this file while the server is stopped.

## Tools
| Tool | Actual behavior |
|---|---|
| Network planner | VLSM allocation, VLAN validation, gateway/client capacity, Cisco config text |
| Configuration audit | Redacted diff and five explicit Cisco IOS baseline checks |
| Security log triage | Time-window failed-login detection, success-after-failure alerts, rejected-line report |
| Endpoint baseline | Firewall, free-disk and inventory-age checks on imported observations |
| Data pipeline & BI | CSV validation, SQLite upserts, priority summaries, resolved-ticket SLA charts |
| Knowledge sources | Persistent FTS5 document indexing |
| Knowledge assistant | Ranked excerpts with source IDs; optional Ollama answer generation |
| Service monitor | Bounded HTTP probes against operator-configured URLs |

Example data is synthetic and loaded only when requested. The network output combines switch VLAN and router subinterface commands; split it per device and review interface names. It does not configure live equipment. Security findings are triage signals, not proof of compromise. Endpoint baseline success does not certify patch/antivirus compliance.

## FastAPI runtime
```sh
python -m pip install -r requirements.txt
```
Set a random `OPS_TOKEN` of at least 32 characters, then:
```sh
python -m uvicorn asgi:app --host 127.0.0.1 --port 8090
```
Use the same browser UI. `/docs` documents the generic API dispatcher; routes and payloads are illustrated in `web/app.js` and unit tests. FastAPI is an optional server adapter, not a requirement for the download-free runtime.

## Local AI / monitoring
Install Ollama separately, pull a model supported by your hardware, set `OLLAMA_MODEL` to its installed name, restart Ops Studio, add source documents and enable the local-model checkbox. Source excerpts are sent only to `http://127.0.0.1:11434/api/chat`. Without a configured model the assistant is explicitly labelled retrieval. LLM generation has not been validated against a connected model in the authoring environment.

`OPS_MONITOR_TARGETS` accepts a JSON object mapping display names to operator-approved HTTP URLs, at most ten. The UI cannot submit arbitrary target URLs. Checks occur on demand; results are snapshots, not availability percentages. Example: `{"API":"http://127.0.0.1:8090/api/health"}`. Redirects are not followed.

## Tests
```sh
python -m unittest discover -s tests -v
```
Tests cover subnet overflow, injection rejection, credential redaction, time windows, endpoint freshness, ETL idempotency, persistent retrieval and actual HTTP authorization/API calls.

The standard-library server is intended for local use. Shared deployment needs TLS, individual accounts/roles, operational retention and hardened ingress. No cloud resource, endpoint, switch or account is altered by running this app.
