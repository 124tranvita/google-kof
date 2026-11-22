---
type: Regression Map
title: What to retest when payment allocation changes
description: Areas affected when changing PaymentAllocationService, the balance formula or allocation operations, with reasons and code evidence.
tags: [regression, payment, allocation]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: alloc-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/Application/PaymentAllocationService.php
    title: PaymentAllocationService
  - id: balance-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/InvoiceBalanceService.php
    title: InvoiceBalanceService
---

# Scope of change

Changing payment allocation, `recalculate`, or the screens/APIs that create, edit or delete payments. Source rules: [allocation](/domain/business-rules/payment-allocation-rules.md), [balance recalculation](/domain/business-rules/balance-recalculation.md).

# Affected areas

| # | Area | Why affected | What to test | Evidence |
|---|---|---|---|---|
| 1 | Invoice balance and status | Allocation changes `due_amount`, `status`, `paid_status`, and clears the `overdue` flag | Every status transition in the rule's table; both old and new invoices when moving an allocation | `InvoiceBalanceService::recalculate` |
| 2 | Staff notification when an invoice is fully paid | The `InvoicePaid` event has a listener | Emitted only when it **just** became `PAID`, not for credit notes, not again when an allocation is edited but the invoice stays `PAID` | `NotifyStaff::invoicePaid` |
| 3 | Tax report | Counts only invoices with `paid_status = PAID` | An allocation that makes an invoice become or stop being `PAID` changes the report figure | `Tax::scopeInvoicesBetween` |
| 4 | Invoice edit lock | `allow_edit` reads `paid_status` | The invoice is locked/unlocked under the 3 `retrospective_edits` modes | `Invoice::getAllowEditAttribute` |
| 5 | Invoice deletion | An invoice with payments cannot be deleted | Delete before/after removing the allocation | `DeleteInvoiceRequest` |
| 6 | Credit notes | The credit limit depends on what was collected | Credit after a partial and after a full collection | `CreditNoteService::create` |
| 7 | Manual `COMPLETED` status change | Based on the sum of allocations and credits | Call `COMPLETED` with a balance remaining and with none | `InvoiceService::changeStatus` |
| 8 | Overdue scan | Excludes `COMPLETED` invoices | An overdue invoice then fully paid: `overdue` goes back to false | `CheckInvoiceStatus`, `recalculate` |
| 9 | Payment receipt PDF | PDF generation is deferred until after the transaction commits | No PDF is generated when the allocation is rejected | test "payment PDF generation is deferred..." |
| 10 | Foreign currency and `base_amount` | `base_amount` is split proportionally, the last row takes the remainder | A foreign-currency payment split across several invoices; check invariant B3 | `PaymentAllocationService::baseAmounts`, `ForeignCurrencyAmountsTest` |
| 11 | Legacy link restore command | Shares the allocation service | Run the command on data with invalid links | `RestoreLegacyPaymentLinks` |
| 12 | Customer statement, customer portal | Shows balances and payment history | Statement figures match `due_amount` | `CustomerStatementTest` (code not read, needs confirmation) |

# Related automated tests in the repo

`tests/Feature/PaymentAllocationTest.php`, `tests/Feature/CustomerStatementTest.php`, `tests/Feature/ForeignCurrencyAmountsTest.php`, `tests/Feature/DomainSpec/ReceivablesDomainTest.php`.
