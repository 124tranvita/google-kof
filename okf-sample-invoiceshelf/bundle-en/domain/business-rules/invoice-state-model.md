---
type: Business Rule
title: Invoice state model
description: Meaning and transition rules of status, paid_status and overdue; manual status change, overdue scan and deletion.
tags: [invoice, status, overdue, delete]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: invoice-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/InvoiceService.php
    title: InvoiceService::changeStatus
  - id: overdue-cmd
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Console/CheckInvoiceStatus.php
    title: CheckInvoiceStatus command
  - id: delete-req
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Http/Requests/DeleteInvoiceRequest.php
    title: DeleteInvoiceRequest
---

# Status axes

| Axis | Values | Set by |
|---|---|---|
| `status` | `DRAFT`, `SENT`, `VIEWED`, `COMPLETED` | Sending mail, the customer opening the link, [balance recalculation](balance-recalculation.md), the change-status API |
| `paid_status` | `UNPAID`, `PARTIALLY_PAID`, `PAID` | Only [balance recalculation](balance-recalculation.md) |
| `overdue` (boolean) | true/false | The daily scan command; balance recalculation clears the flag once fully paid |

# Manual status change

The API `POST /invoices/{invoice}/status` accepts only `SENT` or `COMPLETED`. See the [invoice API](/api/invoices.md).[^invoice-svc]

* `SENT`: sets `status = SENT` and `sent = true`.
* `COMPLETED`: allowed only when the remaining balance is zero (computed from allocations and credit notes) and `due_amount` and `base_due_amount` are both zero. Otherwise it returns the error `invoice_must_be_settled_before_completion`.

> A point to ask dev/BA about while testing: the `SENT` branch sets `status = SENT` unconditionally, so an invoice that is `VIEWED` seems to be moved back to `SENT`. Not verified by a real run.

# Overdue scan

The command `check:invoices:status` sets `overdue = true` when the invoice satisfies **all** of:[^overdue-cmd]

* `type = INVOICE` (credit notes are never overdue).
* `status` is neither `COMPLETED` nor `DRAFT`.
* `overdue` is currently false.
* `due_date` is **earlier than** today (compared by date). An invoice due exactly today is **not** yet overdue.

When it marks an invoice, the system emits the `InvoiceBecameOverdue` event.

# Deleting invoices

The bulk delete API `POST /invoices/delete` takes a list of `ids`. Each id must:[^delete-req]

* exist in `invoices`;
* have **no payment** attached (the `payments` relation);
* if a credit note points to it, that credit note must be **in the same delete batch**, otherwise it is rejected.

[^invoice-svc]: InvoiceService::changeStatus
[^overdue-cmd]: CheckInvoiceStatus (docblock and handle)
[^delete-req]: DeleteInvoiceRequest::rules, the RelationNotExist and CreditNoteDeletedTogether rules
