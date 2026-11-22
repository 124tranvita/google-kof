---
type: API Endpoint
title: Payment allocation API
description: Replace the allocation set of a payment and apply customer credit to invoices.
tags: [api, payment, allocation]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: routes
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/routes/company.php
    title: Receivables routes
  - id: replace-req
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/Http/Requests/ReplacePaymentAllocationsRequest.php
    title: ReplacePaymentAllocationsRequest
  - id: credit-req
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/Http/Requests/CreditAllocationRequest.php
    title: CreditAllocationRequest
---

# Replace a payment's allocations

`PUT /api/v1/payments/{payment}/allocations`

| Field | Rule |
|---|---|
| `allocations` | **must be present** (`present`), array type. An empty array is valid and means the whole payment becomes unapplied credit |
| `allocations[].invoice_id` | required, integer, no duplicates |
| `allocations[].amount` | required, integer, at least 1 (minor units) |

The new set **fully replaces** the old set.

# Apply customer credit

`POST /api/v1/customers/{customer}/credit-allocations`

| Field | Rule |
|---|---|
| `allocations` | required, array, at least 1 element |
| `allocations[].payment_id` | required, integer |
| `allocations[].invoice_id` | required, integer |
| `allocations[].amount` | required, integer, at least 1 |

The submitted rows are **added** to the existing allocations. The payment must belong to the right customer and company.

# Error codes

The full table is in the [payment allocation rules](/domain/business-rules/payment-allocation-rules.md). Example error response:

```json
{ "errors": { "allocations": ["payment_allocation_exceeds_invoice_balance"] } }
```

> The JSON shape above is inferred from `ValidationException::withMessages`; confirm the real format when testing.
