# Sachibara · Engineering Software Collection

18 software projects and integration toolkits spanning application development, networking, systems, cloud delivery, security operations, data/BI, AI-assisted retrieval, mobile and QA. The nine original demos are retained; nine additional packages implement the broader engineering scope. The Python studio contains eight operational tools in one browser application.

## Start with working local software
- **[Ops Studio](python-ops-studio/)**: `python server.py`; open port 8090 and enter the printed operator token. No dependency downloads needed.
- **[Operations Platform API](node-operations-platform/)**: Node 24, `npm start`; SQLite mode works without downloads. The React UI requires npm dependencies.
- **[Batch data pipeline](data-bi-starter/)**: `python pipeline.py examples/tickets.csv`; generates a real SQLite database and BI CSV.
- **[Cloud plan checker](delivery-cloud-lab/)**: `python policy.py examples/unsafe-plan.json`; reports an intentionally unsafe example and exits 1.

## Applications and stack coverage
| Software | Stack / capability | Scope |
|---|---|---|
| [Operations Platform](node-operations-platform/) | React, TypeScript, Node.js, PostgreSQL/SQLite | Accounts, ownership, CRUD, audit, concurrency checks |
| [Next.js Operations Portal](nextjs-operations-portal/) | Next.js App Router, TypeScript | Server rendering, HttpOnly sessions, account/incident forms |
| [Stock Ledger](java-inventory-service/) | Java, Spring Boot, Security, JPA, H2/PostgreSQL | Inventory UI, transactional stock movement history |
| [Asset Lifecycle Console](dotnet-angular-assets/) | C#, .NET, Angular, TypeScript, SQLite | Equipment CRUD, lifecycle and ownership fields |
| [Expense Atlas](laravel-vue-expenses/) | Laravel, PHP, Vue, SQLite | Validated expense CRUD and totals |
| [ServiceSlot](php-service-booking/) | PHP, PDO, SQLite | Service booking queue and status updates |
| [ChangeGate API](ruby-change-api/) | Ruby, Sinatra, SQLite | Authenticated change workflow API |
| [MaintainIQ](codeigniter-maintenance/) | CodeIgniter, PHP, SQLite | Equipment maintenance workflow |
| [Incident Board](react-incident-board/) | React, TypeScript | Standalone offline-first triage board |
| [Service Desk Mobile](mobile-service-desk/) | React Native, Expo, TypeScript | Native client for the Operations API |
| [Ops Studio](python-ops-studio/) | Python, optional FastAPI, SQLite, HTTP | Eight tools detailed below |
| [Delivery & Cloud Lab](delivery-cloud-lab/) | Docker, Kubernetes, Terraform/AWS, Prometheus, Grafana | Deployment configuration, monitoring and plan-review software |
| [Endpoint & Network Toolkit](endpoint-network-toolkit/) | PowerShell, AD, Graph/Intune/Entra, Ansible/Cisco | Inventory, onboarding plans and read-only integrations |
| [Data & BI Starter](data-bi-starter/) | Python, SQL, Power BI DAX, PySpark/Databricks | Batch ETL, analytics output and native platform source |
| [QA Automation Lab](qa-automation-lab/) | Playwright, TypeScript | Browser/API/data workflow tests |
| [Support Library](wordpress-support-library/) | WordPress, PHP | Native searchable knowledge-base plugin |
| [Tech Collection](shopify-tech-collection/) | Shopify, Liquid | Merchant-editable native storefront section |
| [Change Governance](servicenow-change-governance/) | ServiceNow, JavaScript | Native workflow scripts and installation schema |

## Ops Studio tools
1. Network engineering: VLSM allocator, VLAN validation and reviewable Cisco configuration output.
2. Network automation support: configuration diffing and baseline audit with credential redaction.
3. Security operations: failed-login time-window analysis and success-after-failure detection; native Sentinel/Splunk query sources also included.
4. Endpoint management: imported firewall/disk/inventory-age checks, fed by the PowerShell collector.
5. Data engineering / BI: validated CSV imports, SQLite upserts, SLA summaries, charts and exports.
6. Knowledge ingestion: searchable persistent source documents.
7. AI application integration: cited retrieval and optional local Ollama answer generation.
8. SRE: actual HTTP probes against operator-configured targets; continuous monitoring is supplied by the Docker observability stack.

These are practical technology combinations. Alternatives such as Flutter, Azure, Django, SQL Server and Salesforce are not implemented merely because related categories exist. Proprietary platform source requires the named platform; there are no fabricated stores, tenants or live integrations.

## Run and verify
Each directory has prerequisites, commands, expected behavior and limits. [VALIDATION.md](VALIDATION.md) distinguishes executed checks from unverified builds/platform integrations. [Engineering CI](../.github/workflows/engineering.yml) is the requested automatic build/check workflow when enabled on this repository. No cloud resources, live endpoints or paid platform instances are provisioned by cloning or running the local demos.

For a portfolio demonstration, show an actual successful workflow, an invalid-input case, persistence, and the relevant test. The source implementations are demo-grade foundations; production hardening and operational deployment remain separate work. Authored source is under the [MIT license](LICENSE).
