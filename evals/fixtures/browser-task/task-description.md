# Browser Task Request

## What the user wants done

Verify that our staging deployment of the inventory dashboard is working correctly after the latest release (v2.4.1).

## Target URL

https://staging.inventory.example.com/dashboard

## Details

- The dashboard should show the inventory summary table with at least 3 product categories
- The "Last synced" timestamp in the top-right corner should be within the last 24 hours
- The "Low Stock Alerts" panel should be visible and show items where quantity < 10
- The export button (labelled "Export CSV") should be clickable and trigger a file download
- There's a known issue where the chart on the Analytics tab sometimes fails to render — check if it loads

## Credentials

The user will log in manually before handing off. No credentials needed in the prompt.

## Expected values

- Page title: "Inventory Dashboard — Staging"
- Product categories expected: "Electronics", "Furniture", "Office Supplies" (at minimum)
- Version number in footer: "v2.4.1"
- Analytics chart element: `#analytics-chart canvas`
