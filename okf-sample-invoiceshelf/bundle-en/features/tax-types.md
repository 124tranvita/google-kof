---
type: Feature
title: Tax types
description: Configure tax types (percentage/fixed, compound, purchases/sales, EN 16931 code) and their effect on documents and reports.
tags: [feature, tax, tax-type]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: taxation-domain
    resource: https://github.com/InvoiceShelf/InvoiceShelf/tree/c8d10f7/app/Domains/Taxation
    title: Domain Taxation
---

# Hub

| Aspect | See |
|---|---|
| Rules | [Tax types](/domain/business-rules/tax-type-rules.md), [Tax calculation](/domain/business-rules/tax-calculation.md) |
| Data | [tax_types](/data/tax-types.md), [taxes](/data/taxes.md) |
| API | [Tax type API](/api/tax-types.md) |

# Existing automated tests (for reference)

`tests/Feature/DomainSpec/TaxationDomainTest.php`, `tests/Unit/DocumentTaxesTest.php`, `tests/Unit/DocumentTotalsTest.php`.

# Lateral testing

See the [regression map for tax changes](/regression-map/tax-change.md).
