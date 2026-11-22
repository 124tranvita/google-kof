---
type: Regression Map
title: What to retest when credit notes change
description: Areas affected when changing CreditNoteService, CreditNoteAmounts or how a credit note links to its original invoice.
tags: [regression, credit-note]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: credit-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/CreditNoteService.php
    title: CreditNoteService
  - id: invoice-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Models/Invoice.php
    title: Invoice model
---

# Scope of change

Changing credit note creation, the amount-splitting formula, numbering, deletion or display of credit notes. Source rules: [credit note](/domain/business-rules/credit-note-rules.md).

# Affected areas

| # | Area | Why affected | What to test | Evidence |
|---|---|---|---|---|
| 1 | Original invoice balance and status | A credit lowers `due_amount`; a full credit moves the invoice to `COMPLETED`/`PAID` | Partial credit (still `UNPAID`), full credit, credit after a partial collection | `InvoiceBalanceService` |
| 2 | Edit lock | An invoice with a credit note cannot be edited | Edit the original invoice before and after a credit note exists | `Invoice::getAllowEditAttribute` |
| 3 | Payment allocation | What an invoice can still receive subtracts the credited part; a credit note accepts no payments | Allocate to an already credited invoice; allocate to a credit note (expect `payment_allocation_invoice_not_payable`) | `PaymentAllocationService` |
| 4 | Numbering | Credit notes are numbered separately by `credit_note_number_format` | Numbers are sequential, do not clash with invoices, no duplicates on concurrent creation | `CreditNoteService::persist` |
| 5 | Invoice deletion | Must be deleted together with its credit notes in one batch | Delete the original invoice without its credit note (rejected); delete both | `CreditNoteDeletedTogether` |
| 6 | Tax and `base_*` | Split proportionally from stored values | Invariant B6; foreign-currency invoice | `CreditNoteAmounts` |
| 7 | Mail, PDF, customer portal | There are `SendCreditNoteMail` and `CreditNoteResource` | Send a credit note mail; negative amounts display in the right format | `Sales/Mail/SendCreditNoteMail.php` |
| 8 | Reports | **Not surveyed**: unclear whether revenue/tax reports add negative credit notes | A question for dev/BA, then write TCs | |
| 9 | Concurrency | Row lock on the original invoice | Two credit requests at once for the same line | `CreditNoteService::create` |

# Related automated tests in the repo

`tests/Unit/CreditNoteAmountsTest.php`, `tests/Feature/DomainSpec/SalesDomainTest.php`.
