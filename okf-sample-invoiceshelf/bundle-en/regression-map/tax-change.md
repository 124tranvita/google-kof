---
type: Regression Map
title: What to retest when tax calculation or tax types change
description: Areas affected when changing DocumentTotals, Tax, TaxType or a document's tax data.
tags: [regression, tax]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: totals
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Support/DocumentTotals.php
    title: DocumentTotals
  - id: tax-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Models/Tax.php
    title: Tax model
  - id: changelog
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/CHANGELOG.md
    title: CHANGELOG
---

# Scope of change

Changing the total formula, the `tax_per_item`/`tax_included`/compound flags, adding or editing a TaxType, or how `taxes` is stored. Source rules: [tax calculation](/domain/business-rules/tax-calculation.md), [tax types](/domain/business-rules/tax-type-rules.md).

# Affected areas

| # | Area | Why affected | What to test | Evidence |
|---|---|---|---|---|
| 1 | Invoice totals | The server recomputes `sub_total`, `tax`, `total` | The 7 examples in the rule; add flag combinations per the [matrix](/testing/test-design/money-and-rounding.md) | `DocumentTotals`, `DocumentTotalsTest` |
| 2 | Estimates, recurring invoices | Same total mechanism; `taxes` has separate owner columns for estimates and recurring invoices | Create and edit estimates/recurring invoices with per-item and compound tax | `taxes.estimate_id`, `taxes.recurring_invoice_id`; the CHANGELOG mentions consistent calculation for recurring invoices |
| 3 | Clone, estimate ↔ invoice conversion | Must copy the snapshot taxes correctly | Compare totals and each tax line between the original and the new document | `InvoicesController::clone`, `::convertToEstimate`, `EstimatesController::convertToInvoice` |
| 4 | Credit notes | Tax is split proportionally from the stored `taxes.amount` | Partial/full credit; a fully credited invoice reaches 0 to the cent | `CreditNoteAmounts` |
| 5 | PDF, mail, public page | Rendering reads the document's taxes | **Rendering the same document several times in a row must give the same figure** (see the [bug lesson](/bugs/tax-per-line-second-render-inflated.md)) | CHANGELOG #934 |
| 6 | Tax report | Counts only `PAID` invoices; sums `base_amount` by `tax_type_id` | The report total matches the tax total of paid invoices in the period; both invoice-level and line-level taxes | `Tax::scopeInvoicesBetween`, `scopeTaxAttributes` |
| 7 | Expenses (purchases) | `taxes.expense_id`, TaxType has `transaction_type` | Input tax appears correctly in the report; `sales` TaxTypes do not mix with `purchases` | `Tax::scopeExpensesBetween` |
| 8 | Deleting and editing a TaxType | Deletion is blocked while `taxes` rows exist; editing a TaxType does not change old documents | Delete a tax type in use (expect 422 `taxes_attached`); edit the % then reopen an old invoice | `TaxTypesController::destroy`, `Tax` docblock |
| 9 | EN 16931 e-invoice | TaxType has a category code and exemption reason, used by the e-invoicing module | A 0% tax type must set `Z` or `E` with a reason; old data defaults to `S` | CHANGELOG (alpha 13), `TaxType` |
| 10 | Customer portal | There is a separate `TaxResource` for the portal | The tax the customer sees matches the admin side | `Taxation/Http/Resources/CustomerPortal` |

# Related automated tests in the repo

`tests/Unit/DocumentTotalsTest.php`, `tests/Unit/DocumentTaxesTest.php`, `tests/Unit/CreditNoteAmountsTest.php`, `tests/Feature/DomainSpec/TaxationDomainTest.php`.
