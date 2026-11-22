---
type: Feature
title: Invoice management
description: "Navigation hub for the invoice feature: rules, data, API, existing tests and areas needing lateral testing."
tags: [feature, invoice]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: sales-domain
    resource: https://github.com/InvoiceShelf/InvoiceShelf/tree/c8d10f7/app/Domains/Sales
    title: Domain Sales
---

# Purpose

Issue invoices to customers, send them, track collection status, duplicate, convert from/to estimates, recurring invoices, payment reminders.

# Hub

| Aspect | See |
|---|---|
| Terminology | [Invoice](/domain/glossary/invoice.md), [Minor units](/domain/glossary/minor-units.md) |
| Rules | [Status](/domain/business-rules/invoice-state-model.md), [Balance recalculation](/domain/business-rules/balance-recalculation.md), [Tax calculation](/domain/business-rules/tax-calculation.md), [Edit lock](/domain/business-rules/invoice-edit-lock.md) |
| Data | [invoices](/data/invoices.md), [taxes](/data/taxes.md) |
| API | [Invoice API](/api/invoices.md) |
| Flow | [Invoice to cash](/domain/workflows/invoice-to-cash.md) |

# Existing automated tests in the repo (for reference)

`tests/Unit/DocumentTotalsTest.php`, `tests/Unit/InvoiceTest.php`, `tests/Feature/DomainSpec/SalesDomainTest.php`, `tests/Feature/ForeignCurrencyAmountsTest.php`, `tests/Feature/Recurrence/RecurringInvoiceHardeningTest.php`.

# Lateral testing when this feature changes

See the [regression map for tax changes](/regression-map/tax-change.md) and [for payment allocation changes](/regression-map/payment-allocation-change.md). In addition: recurring invoices, duplication, conversion from estimates, PDF/mail, customer portal.
