---
type: Database Table
title: customer_payment_allocations
description: Each row assigns part of a payment to an invoice; the source of the money collected on an invoice.
resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/Models/PaymentAllocation.php
tags: [table, payment, allocation]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: alloc-mig
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_08_02_230400_replace_payment_invoice_with_allocations.php
    title: Migration creating the allocation table
  - id: rename-mig
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_09_27_190911_rename_customer_payment_storage.php
    title: Migration renaming the payment tables
---

# Schema

| Column | Type | Meaning |
|---|---|---|
| `id` | bigIncrements | |
| `payment_id` | unsigned bigint, index | Source payment |
| `invoice_id` | unsigned int, index | Receiving invoice |
| `amount` | unsigned bigint | Allocated amount (minor) |
| `base_amount` | unsigned bigint | Converted to the company currency |
| `created_at`, `updated_at` | | |

* **Unique** `(payment_id, invoice_id)`.
* This table was originally named `payment_allocations`; version 3.0 renamed it to `customer_payment_allocations` (and `payments` to `customer_payments`). Modules that query the table directly must use the new names.
* The `legacy_payment_links` table keeps old invalid links so they can be restored as unapplied credit.

See the [allocation rules](/domain/business-rules/payment-allocation-rules.md).
