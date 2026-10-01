# Support Library for WordPress

Native WordPress plugin: Support Articles custom post type, Support Topics taxonomy, Gutenberg/REST editing support, revisions, article archives and a responsive searchable directory shortcode with topic filters and pagination. Uses WordPress publishing and admin permissions; the public directory returns published articles only.

## Install
1. Copy this entire folder into `wp-content/plugins/wordpress-support-library/` on a local/development WordPress installation.
2. Activate **Sachibara Support Library** in Plugins.
3. Add topics and publish Support Articles in the admin sidebar.
4. Create a page and insert `[support_library]` in a Shortcode block.
5. View the page; search and filter. Articles also have individual permalinks.

Requires PHP 8.1+, a working WordPress site and its database. No WordPress account is connected through this repository. No sample content is inserted automatically; create articles such as “Diagnosing a disconnected LAN port” and “Checking DNS resolution”.

## Verify
Create >9 published articles to test pagination; ensure search/topic query parameters survive page changes. Draft an article and verify public exclusion. Check the logged-out directory and mobile layout. If article permalinks return 404, save Settings → Permalinks. Deactivation leaves editorial content intact. Uninstall does not delete articles; intentional to protect content. The plugin CSS is namespaced but enqueued globally to support shortcode placement in widgets/templates.
