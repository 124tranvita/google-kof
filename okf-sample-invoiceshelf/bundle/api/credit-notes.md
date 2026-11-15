---
type: API Endpoint
title: API tạo credit note
description: POST /invoices/{invoice}/credit-note - tạo credit note toàn phần hoặc từng phần.
tags: [api, credit-note]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: req
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Http/Requests/CreateCreditNoteRequest.php
    title: CreateCreditNoteRequest
---

# Request

`POST /api/v1/invoices/{invoice}/credit-note`

| Trường | Quy tắc |
|---|---|
| `reason` | tùy chọn, chuỗi, tối đa 1000 ký tự |
| `items` | tùy chọn, mảng. **Bỏ trống hoặc rỗng** nghĩa là credit toàn bộ phần còn lại |
| `items[].id` | bắt buộc, số nguyên, không trùng, phải là id dòng **của chính hóa đơn này** |
| `items[].quantity` | bắt buộc, số, lớn hơn 0 |

# Ví dụ

```json
{ "reason": "Khách trả 1 sản phẩm", "items": [ { "id": 42, "quantity": 1 } ] }
```

# Lỗi nghiệp vụ

`invoice_already_fully_credited`, `credit_quantity_exceeds_remaining`, `credit_note_must_credit_something`, `credit_amount_exceeds_invoice_balance`. Điều kiện chi tiết ở [quy tắc credit note](/domain/business-rules/credit-note-rules.md).
