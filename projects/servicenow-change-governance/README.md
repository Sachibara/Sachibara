# Change Governance for ServiceNow

Native ServiceNow project for a developer instance: custom change table, roles, audited fields, approval policy Script Include, enforcing Business Rule, and ACL-aware Scripted REST listing. High-risk approval requires a rollback plan. Approved/finalized plans cannot be silently edited. Unit tests exercise the policy outside ServiceNow; platform behavior still needs instance verification.

## Install (developer instance, Global application)
`schema.json` is an installation specification, **not** an importable update set.
1. In a personal developer instance, create roles `u_sachi_change.operator` and `u_sachi_change.approver`. Make approver contain operator. Assign test users appropriately.
2. Create table **Sachibara Change** with exact name `u_sachi_change` and fields/choices/defaults in `schema.json`. Enable auditing. Make title, risk and status mandatory. Do not extend Task for this demo.
3. Create table-level read/create/write ACLs requiring operator, and deny delete to ordinary operators. Create wildcard field ACLs matching these permissions. Set write ACL on `u_requested_by` to admin only; the Business Rule sets it on insert. Verify any generated ACLs rather than relying solely on roles in scripts.
4. Create non-client-callable Script Include **ChangePolicy**, using `scripts/ChangePolicy.js`.
5. Create Advanced **before** Business Rule on the table for insert and update, order 100, with `scripts/before-change-update.js`.
6. Add application menu/list module for the table, visible to operator. Configure form with all fields and list with title, risk, status, requested by. Role-separate operator and approver users for testing.
7. Create Scripted REST API `sachi_change` with a GET resource `/changes`, paste `scripts/get-changes.js`. Require authentication on API/resource and create a `REST_Endpoint` ACL requiring operator. Use the generated endpoint URI displayed by your instance; do not guess the namespace/version.
8. Capture records in a new update set for export after verification; do not import into a production instance without review.

## Verify
`node --test tests/*.test.mjs` checks policy rules. In the instance, impersonate a non-operator and verify denial; operator creates Draft; operator cannot approve/reject; approver cannot approve High without plan; approver adds plan and approves; operator implements; attempted terminal/approved plan edits are rejected. Check audit history, REST role denial, invalid filter (400), and valid ACL-filtered listing (maximum 100).

No ServiceNow instance is connected or provisioned here. Scripts use exact Global names above. Scoped installation requires replacing table/role names and Script Include namespace; do not paste unchanged into an arbitrary scoped app. This learning project does not implement production change management, separation of requester/approver identities, maintenance windows, notifications or the platform's built-in Change application.
