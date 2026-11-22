---
type: API Endpoint
title: Tax type API
description: CRUD of the company's tax-types, including validation, the PUT/PATCH quirk and the delete error.
tags: [api, tax, tax-type]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: routes
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/routes/company.php
    title: Taxation routes
  - id: req
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Http/Requests/TaxTypeRequest.php
    title: TaxTypeRequest
---

# Endpoints

| Method | Path |
|---|---|
| GET | `/api/v1/tax-types` (supports `search`, `transaction_type`, `limit=all`) |
| POST | `/api/v1/tax-types` |
| GET | `/api/v1/tax-types/{tax_type}` |
| PUT, PATCH | `/api/v1/tax-types/{tax_type}` |
| DELETE | `/api/v1/tax-types/{tax_type}` |

# Payload

| Field | Rule |
|---|---|
| `name` | required, unique within the company (type `GENERAL`) |
| `calculation_type` | required: `percentage` or `fixed` |
| `percent`, `fixed_amount` | number, optional |
| `compound_tax` | boolean, optional |
| `transaction_type` | `sales` or `purchases`, optional |
| `tax_category_code` | one of `S, Z, E, AE, K, G, O, L, M` |
| `tax_exemption_reason` | string, at most 255 |

# Behaviour to test

* `PUT` with an unchanged name: valid. `PATCH` with an unchanged name: reported as a duplicate. See the [tax type rules](/domain/business-rules/tax-type-rules.md).
* `DELETE` of a tax type already in use: **HTTP 422** with `{"error": "taxes_attached", "message": "Taxes Attached."}`.
