---
type: Feature
title: Credit note
description: Create a full or partial credit note for an invoice and keep balances in sync.
tags: [feature, credit-note]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: credit-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/CreditNoteService.php
    title: CreditNoteService
---

# Hub

| Aspect | See |
|---|---|
| Terminology | [Credit note](/domain/glossary/credit-note.md) |
| Rules | [Credit note rules](/domain/business-rules/credit-note-rules.md), [Balance recalculation](/domain/business-rules/balance-recalculation.md), [Edit lock](/domain/business-rules/invoice-edit-lock.md) |
| API | [Credit note API](/api/credit-notes.md) |
| Data | [invoices](/data/invoices.md) |

# Existing automated tests (for reference)

`tests/Unit/CreditNoteAmountsTest.php` (amount calculation), `tests/Feature/DomainSpec/SalesDomainTest.php`.

# Lateral testing

See the [regression map for credit note changes](/regression-map/credit-note-change.md).
