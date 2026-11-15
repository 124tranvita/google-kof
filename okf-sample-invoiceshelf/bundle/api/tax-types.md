---
type: API Endpoint
title: API loại thuế
description: CRUD tax-types của công ty, gồm validation, quirk PUT/PATCH và lỗi khi xóa.
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

# Endpoint

| Method | Đường dẫn |
|---|---|
| GET | `/api/v1/tax-types` (hỗ trợ `search`, `transaction_type`, `limit=all`) |
| POST | `/api/v1/tax-types` |
| GET | `/api/v1/tax-types/{tax_type}` |
| PUT, PATCH | `/api/v1/tax-types/{tax_type}` |
| DELETE | `/api/v1/tax-types/{tax_type}` |

# Payload

| Trường | Quy tắc |
|---|---|
| `name` | bắt buộc, duy nhất trong công ty (loại `GENERAL`) |
| `calculation_type` | bắt buộc: `percentage` hoặc `fixed` |
| `percent`, `fixed_amount` | số, tùy chọn |
| `compound_tax` | boolean, tùy chọn |
| `transaction_type` | `sales` hoặc `purchases`, tùy chọn |
| `tax_category_code` | một trong `S, Z, E, AE, K, G, O, L, M` |
| `tax_exemption_reason` | chuỗi, tối đa 255 |

# Hành vi cần test

* `PUT` giữ nguyên tên: hợp lệ. `PATCH` giữ nguyên tên: bị báo trùng. Xem [quy tắc loại thuế](/domain/business-rules/tax-type-rules.md).
* `DELETE` loại thuế đã được dùng: **HTTP 422** với `{"error": "taxes_attached", "message": "Taxes Attached."}`.
