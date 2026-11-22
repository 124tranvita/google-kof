---
type: Test Template
title: API TC template
description: Standard structure of an API TC (request, status code, body, DB check), with a filled-in example.
tags: [testing, template, api]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

# Structure

```markdown
## <ID> - <Action + condition → result>

| Item | Content |
|---|---|
| Type / Priority | ... |
| Endpoint | <METHOD> <path> |
| Related rule | <concept link> |
| Headers | Authorization, company |

**Precondition**: <required data, with ids>
**Request body**: <full JSON>
**Expected result**
- HTTP status:
- Body (key fields):
- DB after the call:
**Side-effect check** (negative TC)
```

# Filled-in example

## INV-ALLOC-API-001 - PUT allocations with a sum greater than the payment amount is rejected

| Item | Content |
|---|---|
| Type / Priority | Negative / P1 |
| Endpoint | `PUT /api/v1/payments/{payment}/allocations` ([allocation API](/api/payment-allocations.md)) |
| Related rule | [Allocation rules](/domain/business-rules/payment-allocation-rules.md), row #4 |
| Headers | `Authorization: Bearer <token>`, `company: <id of company A>` |

**Precondition**
- Invoices I1 and I2 in the same company, same customer, same currency, `status = SENT`, each with `total = 100`.
- Payment P1 of the same customer and currency, `amount = 100`, not yet allocated.

**Request body**
```json
{ "allocations": [ { "invoice_id": <I1>, "amount": 60 }, { "invoice_id": <I2>, "amount": 50 } ] }
```

**Expected result**
- HTTP status: 422 (the Laravel default for validation errors; confirm when running).
- Body: an error containing `payment_allocation_exceeds_payment_amount` on the field `allocations`.
- DB: no row in `customer_payment_allocations` for P1.

**Side-effect check**
- `due_amount` of I1 and I2 is still 100; `paid_status` is still `UNPAID`.

# Variants to generate along with it

One TC for each row of the rule's error-code table, plus TCs for a missing field, a wrong type (`amount` = "abc", 0, -1), `allocations` absent (violating `present`), a duplicate `invoice_id`, and the `company` header of another company.
