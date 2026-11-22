---
type: Business Rule
title: Tax type rules
description: A tax type defines how tax is calculated; a Tax on a document is a snapshot; deletion constraint, duplicate names, EN 16931 codes.
tags: [tax, tax-type, validation, en16931]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: taxtype-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Models/TaxType.php
    title: TaxType model
  - id: tax-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Models/Tax.php
    title: Tax model
  - id: taxtype-req
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Http/Requests/TaxTypeRequest.php
    title: TaxTypeRequest
  - id: taxtype-ctl
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Http/Controllers/TaxTypesController.php
    title: TaxTypesController
---

# Two concepts

* **TaxType** (`tax_types`): the company's tax definition. The calculation is `percentage` or `fixed`, it belongs to the `sales` or `purchases` side, and it is compound (`compound_tax`) or not.[^taxtype-model]
* **Tax** (`taxes`): one tax applied to one object. It is a **snapshot**: name, percentage, calculation mode, fixed amount and the compound flag are copied from the TaxType at application time, so editing the TaxType later does **not** change old documents.[^tax-model] Each `taxes` row is attached to only **one** owner (invoice, invoice item, recurring invoice, expense or catalog item).

# Constraints

| Rule | Behaviour |
|---|---|
| A TaxType name (type `GENERAL`) is unique within the company | Validation error on duplicate |
| `calculation_type` is required, either `percentage` or `fixed` | |
| `transaction_type` is `sales` or `purchases` | |
| `tax_category_code` belongs to the EN 16931 set: `S, Z, E, AE, K, G, O, L, M` | |
| `tax_exemption_reason` at most 255 characters | The groups `E, AE, K, G, O` are the ones that require an exemption reason under EN 16931 rules (BT-120); the request currently does **not** enforce entering it |
| Deleting a TaxType that is in use | Rejected: HTTP 422, `{"error": "taxes_attached"}`[^taxtype-ctl] |
| TaxType of type `MODULE` | Belongs to a module, is not shown in the list and is excluded from the duplicate-name check |

# Known quirks (to test correctly)

* The duplicate-name check **skips the record being edited only for method `PUT`**. Sending `PATCH` with an unchanged name is reported as a duplicate of itself.[^taxtype-req]
* The list filter that passes `company_id` only switches filtering on; the actual company comes from the `company` header, not from the submitted value.

# Tax report

The sales tax report counts only `Tax` rows belonging to **invoices with `paid_status = PAID`** and `invoice_date` within the range, both invoice-level and line-level taxes. It needs both `from_date` and `to_date`; if one end is missing it **does not filter**. Expense taxes are filtered by `expense_date` and ignore payment status.[^tax-model]

Therefore any change that alters `paid_status` (see [payment allocation](payment-allocation-rules.md)) affects the tax report.

[^taxtype-model]: TaxType model (docblock)
[^tax-model]: Tax model (docblock and scope `scopeInvoicesBetween`)
[^taxtype-req]: TaxTypeRequest::rules (comment "Quirk kept as is")
[^taxtype-ctl]: TaxTypesController::destroy and helper respondJson (HTTP 422)
