---
type: Business Rule
title: Payment allocation rules
description: Conditions for a payment to be allocated to invoices, the matching error codes, atomicity and the split of base_amount.
tags: [payment, allocation, validation, error-codes]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: alloc-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/Application/PaymentAllocationService.php
    title: PaymentAllocationService
  - id: alloc-test
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/tests/Feature/PaymentAllocationTest.php
    title: PaymentAllocationTest
---

# Validity conditions and error codes

Error codes are returned in `errors.allocations` (or `errors.amount`).[^alloc-svc]

| # | Violated condition | Error code |
|---|---|---|
| 1 | Duplicate `invoice_id` in the same request | `payment_allocation_duplicate_invoice` |
| 2 | Missing `invoice_id`/`amount`, not an integer, `invoice_id < 1` or `amount < 1` | `payment_allocation_invalid` |
| 3 | `payment.amount < 1` | `payment_amount_must_be_positive` (on `amount`) |
| 4 | Sum of allocations is greater than `payment.amount` | `payment_allocation_exceeds_payment_amount` |
| 5 | An `invoice_id` does not exist | `payment_allocation_invoice_not_found` |
| 6 | The invoice has a different **company**, **customer** or **currency** than the payment | `payment_allocation_invoice_mismatch` |
| 7 | The invoice is a credit note, or is `DRAFT` | `payment_allocation_invoice_not_payable` |
| 8 | `amount` is greater than what the invoice can still receive | `payment_allocation_exceeds_invoice_balance` |

"What an invoice can still receive" = `max(0, total - credited - sum of allocations from other payments)`.

For the apply-credit endpoint (see the [allocation API](/api/payment-allocations.md)):

| Condition | Error code |
|---|---|
| The `allocations` list is empty | `payment_allocation_required` |
| The payment does not belong to this company/customer | `payment_allocation_payment_not_found` |

# Behaviour

* **Full replacement** (`replace`): the new set of allocations completely replaces the old set. An empty list is valid (everything becomes unapplied credit).
* **Apply credit** (`applyCustomerCredits`): the submitted rows are **added** to the existing allocations; the old ones are not removed.
* **Atomic**: runs in one transaction; invoices are locked in ascending id order to avoid deadlocks and to avoid two requests both "spending" the same balance. If rejected, **no** allocation changes and `due_amount` stays the same.[^alloc-test]
* After writing, **every affected invoice (old and new)** gets a [balance recalculation](balance-recalculation.md).
* **Splitting `base_amount`**: split proportionally from the payment's `base_amount`, rounded down. The last row of a fully allocated payment takes the remainder, so the rows' `base_amount` sum equals the payment's `base_amount` exactly.

# TC hints

Each row of the error table above is one negative TC. See the [API TC template](/testing/tc-templates/api.md) and [good vs bad TC examples](/testing/good-vs-bad-tc.md).

[^alloc-svc]: PaymentAllocationService (normaliseAllocations, assertAllocationTotal, assertInvoiceCanReceiveAllocation, assertCreditRows, baseAmounts)
[^alloc-test]: PaymentAllocationTest, case "allocation over an invoice balance is rejected without changing allocations"
