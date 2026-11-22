---
type: Workflow
title: Invoice to cash
description: End-to-end flow of creating an invoice, sending it, collecting payment, allocating, crediting and closing, with the status at each step.
tags: [workflow, invoice, payment]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: readme
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/README.md
    title: README
---

# Main flow

| Step | Action | `status` | `paid_status` | Applicable rules |
|---|---|---|---|---|
| 1 | Create invoice (draft) | `DRAFT` | `UNPAID` | [Total calculation](../business-rules/tax-calculation.md) |
| 2 | Send to customer | `SENT` | `UNPAID` | [Status](../business-rules/invoice-state-model.md) |
| 3 | Customer opens the link | `VIEWED` | `UNPAID` | |
| 4 | Record a payment, allocate part of it | `VIEWED` | `PARTIALLY_PAID` | [Allocation](../business-rules/payment-allocation-rules.md), [Balance recalculation](../business-rules/balance-recalculation.md) |
| 5 | Allocate the remainder | `COMPLETED` | `PAID` | emits the `InvoicePaid` event |
| 6 | Past due without full payment | unchanged | unchanged | `overdue = true` set by the scan command |

# Branches

* **Overpayment**: the unallocated part is customer credit, later applied to another invoice of the same customer and currency.
* **Credit note**: reduces the original invoice's balance and locks editing. See [credit note rules](../business-rules/credit-note-rules.md).
* **Recurring invoices**: generate invoices on a schedule; there are `RecurringInvoiceGenerated` and `RecurringInvoiceFailed` events.
* **Reminders**: payment-reminder settings exist per company and per invoice (`reminders_paused`).

> Steps 1 to 3 are inferred from status constants and commands in the code. Compare against the real screens to confirm the order.

# End-to-end TC to have

At least one TC that runs through steps 1 to 5 and checks the status at each step. See the [functional TC template](/testing/tc-templates/functional.md).
