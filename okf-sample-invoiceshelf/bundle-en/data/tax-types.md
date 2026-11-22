---
type: Database Table
title: tax_types
description: "The company's tax type definitions: calculation mode, purchases/sales side, compound, EN 16931 code."
resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Models/TaxType.php
tags: [table, tax, tax-type]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: base-schema
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_01_01_000000_consolidate_base_schema.php
    title: Base migration
  - id: en-mig
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_10_24_120000_add_en16931_codes_to_tax_types_and_units.php
    title: EN 16931 codes migration
---

# Schema

| Column | Type | Meaning |
|---|---|---|
| `name` | string | Unique within the company (only for type `GENERAL`) |
| `calculation_type` | enum `percentage`/`fixed` | Default `percentage` |
| `percent` | decimal(5,2), null | Used when `percentage` |
| `fixed_amount` | integer, null | Used when `fixed`, in minor units |
| `compound_tax` | tinyint, default 0 | Stacks on top of other taxes |
| `collective_tax` | tinyint, default 0 | |
| `type` | enum `GENERAL`/`MODULE` | `MODULE` is managed by a module |
| `transaction_type` | string(20) | `sales` or `purchases`. Old data was placed in `sales` |
| `tax_category_code` | string(4), default `S` | EN 16931 code (UNTDID 5305) |
| `tax_exemption_reason` | string(255), null | Exemption reason (BT-120) |
| `description`, `company_id` | | |

See the [tax type rules](/domain/business-rules/tax-type-rules.md) and the [tax type API](/api/tax-types.md).
