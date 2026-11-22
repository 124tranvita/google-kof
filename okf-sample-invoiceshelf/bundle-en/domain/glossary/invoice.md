---
type: Glossary Term
title: Invoice
description: A billing document issued to a customer; one table holds both regular invoices and credit notes.
tags: [glossary, invoice]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: invoice-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Models/Invoice.php
    title: Invoice model
---

# Definition

A record in the `invoices` table. The `type` column distinguishes two document types:

| `type` | Meaning |
|---|---|
| `INVOICE` | Regular invoice, positive amounts |
| `CREDIT_NOTE` | Reverses an invoice, negative amounts, `related_invoice_id` points to the original. See [credit note](credit-note.md) |

Each document has **two independent status axes**:[^invoice-model]

* `status`: progress of sending to the customer (`DRAFT`, `SENT`, `VIEWED`, `COMPLETED`).
* `paid_status`: money collected (`UNPAID`, `PARTIALLY_PAID`, `PAID`).

These axes are **not set by hand**; they are derived again every time the balance changes. Details in the [state model](../business-rules/invoice-state-model.md) and [balance recalculation](../business-rules/balance-recalculation.md).

# Related

* Money is stored in [minor units](minor-units.md).
* Has line items (`invoice_items`) and taxes (`taxes`). See [tax calculation](../business-rules/tax-calculation.md).
* Data: [invoices table](/data/invoices.md).

[^invoice-model]: Invoice model (class docblock)
