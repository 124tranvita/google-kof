---
type: Feature
title: Recording and allocating payments
description: Record customer payments, split them across invoices, keep the remainder as credit and apply credit later.
tags: [feature, payment, allocation]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: receivables-domain
    resource: https://github.com/InvoiceShelf/InvoiceShelf/tree/c8d10f7/app/Domains/Receivables
    title: Domain Receivables
---

# Purpose

Collect money from customers, assign it to invoices, manage unapplied credit, send receipt mail/PDF.

# Hub

| Aspect | See |
|---|---|
| Terminology | [Payment allocation](/domain/glossary/payment-allocation.md) |
| Rules | [Payment allocation](/domain/business-rules/payment-allocation-rules.md), [Balance recalculation](/domain/business-rules/balance-recalculation.md) |
| Data | [customer_payment_allocations](/data/customer-payment-allocations.md) |
| API | [Allocation API](/api/payment-allocations.md) |

# Existing automated tests (for reference)

`tests/Feature/PaymentAllocationTest.php` (multi-invoice, over balance, wrong currency/customer/draft/credit note, duplicates, atomic, legacy data migration), `tests/Feature/Receivables/PaymentComposerTest.php`, `tests/Unit/PaymentTest.php`.

# Lateral testing

See the [regression map for payment allocation changes](/regression-map/payment-allocation-change.md).
