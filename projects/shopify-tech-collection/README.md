# Tech Collection for Shopify

Native Liquid section for an Online Store 2.0 theme. Merchant-editable collection, headings, colors and product count; responsive product cards; lazy-loaded images; per-variant price and availability; native Shopify add-to-cart forms; unique IDs and section-scoped styles. This is a theme extension section, not a complete Shopify theme or a simulated store.

## Install in a development store
1. Duplicate the store's theme for testing.
2. In Edit code, add `sections/tech-collection.liquid` with the provided contents.
3. In Customize, add **Tech collection** to a supported JSON-template page.
4. Select a collection containing published products available to the Online Store channel; save.
5. Test variant selection and Add to cart through the theme's native cart flow.

No Shopify store is connected or created by this repository. Product/catalog/cart/checkout functionality comes from Shopify. Compatible with section-capable Online Store 2.0 themes such as Dawn; not a checkout extension. No purchases are required for the showcase.

## Verify
Run `shopify theme check` in the full theme directory. Test no collection, empty collection, product without image, single/multiple variants, unavailable variant, entirely sold-out product, two copies of the section, theme editor changes and a mobile viewport. Native forms avoid a custom cart API implementation. Colors are editable; choose combinations with sufficient contrast. The section shows a curated subset and links to the full collection.
