---
type: Database Table
title: taxes
description: Tax applied to an object (snapshot from tax_types); signed amounts.
resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Models/Tax.php
tags: [table, tax]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: base-schema
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_01_01_000000_consolidate_base_schema.php
    title: Base migration
  - id: expense-mig
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_08_01_233036_add_expense_id_to_taxes_table.php
    title: Migration adding expense_id
---

# Schema

| Column | Type | Meaning |
|---|---|---|
| `tax_type_id` | int, required | The tax type the snapshot came from. A TaxType that is still referenced cannot be deleted |
| `invoice_id` / `invoice_item_id` | int, null | Invoice-level or line-level tax |
| `estimate_id` / `estimate_item_id` / `item_id` / `recurring_invoice_id` / `expense_id` | int, null | Other owners |
| `name` | string | Name copied from the TaxType at application time |
| `percent` | decimal(5,2), null | Percentage copied from the TaxType |
| `compound_tax` | tinyint | Compound flag copied from the TaxType |
| `amount` | bigint | Tax amount, **signed** (negative for credit notes) |
| `base_amount` | bigint, null | Converted to the company currency |
| `exchange_rate`, `currency_id` | | |

The model also has `fixed_amount` and the calculation mode (`calculation_type`), snapshotted together.

# Rules

* **Exactly one** owner column is filled for each row.
* The tax report sums `base_amount` by `tax_type_id`. See [tax type rules](/domain/business-rules/tax-type-rules.md).
