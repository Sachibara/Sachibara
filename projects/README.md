# Sachibara · Engineering Projects

Nine distinct portfolio demos covering ReactJS/React, .NET, PHP, Laravel, Angular, WordPress, Ruby, TypeScript, CodeIgniter, VueJS, Shopify, ServiceNow, frontend, backend and fullstack development. Authored for Jim Rodmark Camus. React and ReactJS refer to the same library; frontend/backend/fullstack are project roles rather than extra frameworks.

| Project | Stack / role | Implemented behavior |
|---|---|---|
| [Incident Command Board](react-incident-board/) | React + TypeScript · Frontend | Incident triage, search, priority, local persistence, validated backup import/export |
| [Asset Lifecycle Console](dotnet-angular-assets/) | .NET 10 + Angular + TypeScript · Fullstack | Equipment CRUD, owner search, lifecycle tracking, unique tags, EF Core SQLite |
| [Expense Atlas](laravel-vue-expenses/) | Laravel + PHP + VueJS · Fullstack | Expense CRUD, category totals, integer centavos, validation, CSRF, SQLite |
| [ServiceSlot](php-service-booking/) | PHP · Backend + server-rendered frontend | Service request queue, booking dates, search, status updates, PDO SQLite |
| [ChangeGate API](ruby-change-api/) | Ruby + Sinatra · Backend | Authenticated change-request API, validated state transitions, SQLite |
| [MaintainIQ](codeigniter-maintenance/) | CodeIgniter + PHP · Fullstack MVC | Maintenance job queue, priority, status filtering, CSRF forms, SQLite |
| [Support Library](wordpress-support-library/) | WordPress + PHP · CMS / frontend | Native plugin, custom articles/topics, editor support, search, pagination |
| [Tech Collection](shopify-tech-collection/) | Shopify Liquid · Storefront frontend | Merchant-editable section, variants, native add-to-cart, responsive cards |
| [Change Governance](servicenow-change-governance/) | ServiceNow + JavaScript · Platform backend | Custom table/roles specification, approval rules, audited records, secured REST listing |

## Getting started
Clone `Sachibara/Sachibara`, enter `projects/`, choose a project and follow its README. Each is independently installable; there is no shared database or required cloud account for the six general web/API projects. WordPress, Shopify and ServiceNow need their respective development environments.

Laravel and CodeIgniter include complete project-specific MVC code in `overlay/` and a safe Python setup script that installs the official framework shell into ignored `runtime/`. Third-party framework dependencies are not vendored. The other projects include source and native manifests directly. Public-facing dashboards are local demos; consult each guide before exposing a server.

## Verification
```sh
python tests/validate_collection.py
node --test react-incident-board/tests/*.test.mjs servicenow-change-governance/tests/*.test.mjs
```
Read [VALIDATION.md](VALIDATION.md) for checks that actually ran and checks still requiring dependency installation or a platform instance. [ci/portfolio.yml](ci/portfolio.yml) is an optional manual GitHub Actions workflow template. No live deployment is implied.

## Demonstration suggestions
Each README contains a short walkthrough and negative-input checks. Record the actual application, show a valid change, reject an invalid input, then show persistence after refresh/restart. Explain the source structure and limits instead of presenting these as commercial production systems.

## Official references
- [React](https://react.dev/learn) · [TypeScript](https://www.typescriptlang.org/docs/) · [Angular bootstrap](https://angular.dev/api/platform-browser/bootstrapApplication)
- [ASP.NET Core Minimal API](https://learn.microsoft.com/en-us/aspnet/core/tutorials/min-web-api?view=aspnetcore-10.0)
- [Laravel installation](https://laravel.com/docs/12.x/installation) · [Vue](https://vuejs.org/guide/introduction.html)
- [CodeIgniter AppStarter](https://codeigniter.com/user_guide/installation/installing_composer.html)
- [WordPress custom post types](https://developer.wordpress.org/reference/functions/register_post_type/)
- [Shopify section schema](https://shopify.dev/docs/storefronts/themes/architecture/sections/section-schema)
- [ServiceNow Scripted REST API](https://www.servicenow.com/docs/r/api-reference/rest-api-explorer/c_CustomWebServices.html)
- [Sinatra](https://sinatrarb.com/intro.html)

MIT license for this project's authored source. Frameworks/platforms retain their own licenses and terms.
