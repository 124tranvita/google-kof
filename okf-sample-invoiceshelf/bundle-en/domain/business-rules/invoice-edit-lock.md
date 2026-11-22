---
type: Business Rule
title: Invoice edit lock (retrospective_edits)
description: When an invoice can no longer be edited, depending on credit notes and the company's retrospective_edits setting.
tags: [invoice, edit, company-setting]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: invoice-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Models/Invoice.php
    title: Invoice::getAllowEditAttribute
---

# Rule

The invoice's `allow_edit` attribute is computed as follows:[^invoice-model]

1. An invoice that **already has a credit note** can **never be edited** (its line item ids anchor the credit note lines).
2. Otherwise, it depends on the company setting `retrospective_edits`:

| Setting value | Cannot be edited when |
|---|---|
| `disable_on_invoice_sent` | `status` is one of `DRAFT/SENT/VIEWED/COMPLETED` **and** `paid_status` is `PARTIALLY_PAID` or `PAID` |
| `disable_on_invoice_partial_paid` | `paid_status` is `PARTIALLY_PAID` or `PAID` |
| `disable_on_invoice_paid` | `paid_status` is `PAID` |
| any other value / not set | always editable |

# Point to confirm with dev

The `status` list in the `disable_on_invoice_sent` branch contains all 4 values, so in practice this branch **seems to give the same result as** `disable_on_invoice_partial_paid`. The code docblock describes "three progressively stricter steps", so ask about the expected behaviour before writing a TC that distinguishes these two modes.

# TC hints

A matrix of 3 setting values × 3 `paid_status` values × with/without a credit note. See [TC design](/testing/test-design/money-and-rounding.md) on how to build the data.

[^invoice-model]: Invoice::getAllowEditAttribute (docblock and function body)
