---
type: Test Template
title: Functional TC template
description: Standard structure of a functional TC, with a filled-in example about payment allocation.
tags: [testing, template, functional]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

# Structure

```markdown
## <ID> - <Action + condition → result>

| Item | Content |
|---|---|
| Type | Positive / Negative / Boundary |
| Priority | P1 / P2 / P3 |
| Related rule | <link to a concept in the bundle> |

**Precondition (data state)**
- ...

**Test data**
| Name | Displayed value | Stored value |

**Steps**
1. <Verb + object + data>
2. ...

**Expected result**
- <verifiable result: value, error code, status, DB>

**State check after the test** (required for negative TCs)
- ...
```

For how to fill it in, see the [step conventions](../step-conventions.md).

# Filled-in example

## INV-ALLOC-003 - Reject allocation when the amount exceeds the invoice balance

| Item | Content |
|---|---|
| Type | Negative / Boundary |
| Priority | P1 |
| Related rule | [Payment allocation rules](/domain/business-rules/payment-allocation-rules.md), row #8 |

**Precondition**
- Company A, customer KH01, currency USD.
- Invoice INV-0001: type `INVOICE`, `status = SENT`, `total = 100`, `due_amount = 100`, no allocation yet.
- Payment PAY-0001 of KH01, USD, `amount = 101`, no allocation yet.

**Test data**

| Name | Displayed value | Stored value |
|---|---|---|
| Invoice balance | 1.00 | 100 |
| Payment amount | 1.01 | 101 |
| Allocation amount | 1.01 | 101 |

**Steps**
1. Open PAY-0001 and choose to allocate to invoice INV-0001.
2. Enter the allocation amount 1.01 (101).
3. Save the allocation.

**Expected result**
- The system rejects with the error code `payment_allocation_exceeds_invoice_balance`.

**State check after the test**
- No record in `customer_payment_allocations` for PAY-0001.
- INV-0001 still has `due_amount = 100`, `paid_status = UNPAID`.

> This example follows the existing automated test in the repo ("allocation over an invoice balance is rejected without changing allocations"). Screen and button names in steps 1 to 3 must be replaced with the real names from the project's UI spec.
