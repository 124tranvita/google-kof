---
type: API Endpoint
title: Create credit note API
description: POST /invoices/{invoice}/credit-note - create a full or partial credit note.
tags: [api, credit-note]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: req
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Http/Requests/CreateCreditNoteRequest.php
    title: CreateCreditNoteRequest
---

# Request

`POST /api/v1/invoices/{invoice}/credit-note`

| Field | Rule |
|---|---|
| `reason` | optional, string, at most 1000 characters |
| `items` | optional, array. **Omitted or empty** means credit the entire remainder |
| `items[].id` | required, integer, no duplicates, must be the id of a line **of this same invoice** |
| `items[].quantity` | required, number, greater than 0 |

# Example

```json
{ "reason": "Customer returned 1 product", "items": [ { "id": 42, "quantity": 1 } ] }
```

# Business errors

`invoice_already_fully_credited`, `credit_quantity_exceeds_remaining`, `credit_note_must_credit_something`, `credit_amount_exceeds_invoice_balance`. Detailed conditions are in the [credit note rules](/domain/business-rules/credit-note-rules.md).
