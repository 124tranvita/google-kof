---
type: API Endpoint
title: Invoice API
description: Endpoints to create, read, edit, send, clone, change the status of and delete invoices.
tags: [api, invoice]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: routes
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/routes/company.php
    title: Sales routes
  - id: req
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Http/Requests/InvoicesRequest.php
    title: InvoicesRequest
---

# Endpoints

Prefix `/api/v1`, requires the `company` header and a Sanctum token.[^routes]

| Method | Path | Purpose |
|---|---|---|
| GET, POST | `/invoices` | List, create |
| GET, PUT/PATCH | `/invoices/{invoice}` | View, edit |
| POST | `/invoices/delete` | Delete (bulk) `{ids: [...]}`. See the [delete rules](/domain/business-rules/invoice-state-model.md) |
| POST | `/invoices/{invoice}/status` | Change status, `status` is `SENT` or `COMPLETED` |
| POST | `/invoices/{invoice}/send` | Send mail; `GET .../send/preview` for a preview |
| POST | `/invoices/{invoice}/clone` | Duplicate |
| POST | `/invoices/{invoice}/convert-to-estimate` | Convert to an estimate |
| POST | `/invoices/{invoice}/credit-note` | See the [credit note API](credit-notes.md) |
| GET | `/invoices/templates` | List PDF templates |
| GET, POST, PUT | `/invoices/{invoice}/reminders` | Per-invoice payment reminders |

# Create-invoice payload (main rules)

| Field | Rule |
|---|---|
| `invoice_date` | required |
| `customer_id` | required |
| `invoice_number` | required, **unique** |
| `exchange_rate` | required for foreign currency, otherwise optional |
| `discount` | number, required |
| `discount_val` | integer, required |
| `sub_total`, `tax` | required (values are recomputed server-side) |
| `total` | number, required, at most 999999999999 (recomputed server-side) |
| `template_name` | required, must be an existing template |
| `items` | required, array; each element needs `name`, `quantity` (number), `price` (number) |

See [total calculation](/domain/business-rules/tax-calculation.md) to understand why the submitted `total` does not decide the result.

# Points to confirm when testing

`Route::apiResources` also registers the route `DELETE /invoices/{invoice}`, but `InvoicesController` **has no `destroy` method** (only `delete` for `POST /invoices/delete`). Try calling the DELETE route on a real environment to see the result (it may be a 500 error). Deleting an invoice should go through `POST /invoices/delete` because that is where the validation rules apply.

# Business error codes

* `invoice_must_be_settled_before_completion` when setting `COMPLETED` while a balance remains.

[^routes]: Sales routes/company.php
