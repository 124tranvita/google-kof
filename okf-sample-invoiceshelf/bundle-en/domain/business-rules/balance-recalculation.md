---
type: Business Rule
title: Invoice balance recalculation
description: The due_amount formula and how status and paid_status are derived whenever an allocation or credit note changes.
tags: [invoice, balance, due-amount, status]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: balance-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/InvoiceBalanceService.php
    title: InvoiceBalanceService::recalculate
---

# Formula

```
allocated = sum of amount of the allocations attached to the invoice
credited  = - sum of total of the credit notes attached to the invoice   (positive)
due       = max(0, total - allocated - credited)
```

`due_amount = due`, and `base_due_amount` is `due` converted at the exchange rate.[^balance-svc]

# Deriving the status

| Condition | `status` | `paid_status` | `overdue` |
|---|---|---|---|
| `due = 0` | `COMPLETED` | `PAID` | reset to `false` |
| `due > 0` and `allocated > 0` | back to the previous state (`VIEWED` if viewed, `SENT` if sent, otherwise `DRAFT`) | `PARTIALLY_PAID` | unchanged |
| `due > 0` and `allocated = 0` | as above | `UNPAID` | unchanged |

# Points for QA to note

* **A partial credit note does not make the invoice `PARTIALLY_PAID`**, because only `allocated` decides that. An invoice that is only partially credited (no payment) has `paid_status = UNPAID` even though `due_amount` dropped.
* A full credit note makes `due = 0`, so the invoice becomes `COMPLETED` and `PAID` even though no money was collected.
* The `InvoicePaid` event is emitted only when the invoice has **just** changed to `PAID`, it is not a credit note, and `total > 0`. The event is emitted after the transaction commits.
* The caller of this function must hold the invoice's row lock.

This function is called from the [allocation rules](payment-allocation-rules.md) and the [credit note rules](credit-note-rules.md). See the [regression map for allocation changes](/regression-map/payment-allocation-change.md).

[^balance-svc]: InvoiceBalanceService::recalculate
