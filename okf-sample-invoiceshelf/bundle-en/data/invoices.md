---
type: Database Table
title: invoices
description: The table holding both regular invoices and credit notes; meaning of the columns that matter for testing.
resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_01_01_000000_consolidate_base_schema.php
tags: [table, invoice, credit-note]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: base-schema
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_01_01_000000_consolidate_base_schema.php
    title: Base migration
  - id: credit-mig
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_08_02_120000_add_credit_note_support.php
    title: Migration adding credit note support
---

# Schema

Columns present in the base migration or the credit note migration. For columns marked (*), I read them from the model/service and have not checked their migration location; confirm on the real schema.

| Column | Type | Meaning |
|---|---|---|
| `id` | increments | |
| `type` | string, default `INVOICE` | `INVOICE` or `CREDIT_NOTE` |
| `related_invoice_id` | int, null, index | The original invoice of a credit note |
| `credit_reason` | text, null | Reason for the credit |
| `invoice_number` | string | Unique per company; credit notes are numbered separately |
| `invoice_date` | datetime | |
| `due_date` | date, null | Used by the [overdue scan](/domain/business-rules/invoice-state-model.md) |
| `status` | string | `DRAFT/SENT/VIEWED/COMPLETED` |
| `paid_status` | string | `UNPAID/PARTIALLY_PAID/PAID` |
| `overdue` | boolean, default false | Overdue flag |
| `sent`, `viewed` | boolean | Used to go back to the previous status on balance recalculation |
| `tax_per_item`, `discount_per_item` | string `YES`/`NO` | Calculation modes. See [tax calculation](/domain/business-rules/tax-calculation.md) |
| `tax_included`* | boolean | Prices include tax |
| `discount`, `discount_type`, `discount_val` | decimal, string, bigint | Document-level discount |
| `sub_total`, `tax`, `total`, `due_amount` | bigint | [Minor units](/domain/glossary/minor-units.md); credit notes carry negative values |
| `base_discount_val`, `base_sub_total`, `base_tax`, `base_total`, `base_due_amount` | bigint, null | Converted to the company currency |
| `exchange_rate` | decimal(19,6), null | Required when the currency differs from the company currency |
| `currency_id`, `customer_id`, `company_id`, `creator_id`, `recurring_invoice_id` | foreign keys | |
| `sales_tax_type`, `sales_tax_address_type` | string, null | Sales tax mode |
| `unique_hash` | string | PDF share link (anyone with the hash can view) |
| `reminders_paused`* | boolean | Pause payment reminders |

# Relations

* `invoice_items` (column `invoice_id`; credit note lines have `source_invoice_item_id`)
* [taxes](taxes.md) (invoice-level taxes)
* [customer_payment_allocations](customer-payment-allocations.md)
* credit notes: this same table, via `related_invoice_id`

# Constraints worth checking

* `due_amount` must equal `max(0, total - Σ allocation - Σ credit)`. See [balance recalculation](/domain/business-rules/balance-recalculation.md).
* A regular invoice has `total >= 0`; a credit note has a negative total.
