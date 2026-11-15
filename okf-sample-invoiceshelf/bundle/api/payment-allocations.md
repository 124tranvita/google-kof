---
type: API Endpoint
title: API phân bổ thanh toán
description: Thay thế tập phân bổ của một payment và áp dụng tín dụng khách hàng cho hóa đơn.
tags: [api, payment, allocation]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: routes
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/routes/company.php
    title: Receivables routes
  - id: replace-req
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/Http/Requests/ReplacePaymentAllocationsRequest.php
    title: ReplacePaymentAllocationsRequest
  - id: credit-req
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/Http/Requests/CreditAllocationRequest.php
    title: CreditAllocationRequest
---

# Thay thế phân bổ của một payment

`PUT /api/v1/payments/{payment}/allocations`

| Trường | Quy tắc |
|---|---|
| `allocations` | **phải có** (`present`), kiểu mảng. Mảng rỗng hợp lệ, nghĩa là toàn bộ payment thành tín dụng chưa áp dụng |
| `allocations[].invoice_id` | bắt buộc, số nguyên, không trùng |
| `allocations[].amount` | bắt buộc, số nguyên, tối thiểu 1 (minor units) |

Tập mới **thay hẳn** tập cũ.

# Áp dụng tín dụng khách hàng

`POST /api/v1/customers/{customer}/credit-allocations`

| Trường | Quy tắc |
|---|---|
| `allocations` | bắt buộc, mảng, ít nhất 1 phần tử |
| `allocations[].payment_id` | bắt buộc, số nguyên |
| `allocations[].invoice_id` | bắt buộc, số nguyên |
| `allocations[].amount` | bắt buộc, số nguyên, tối thiểu 1 |

Các dòng gửi lên được **cộng thêm** vào phân bổ đang có. Payment phải thuộc đúng khách hàng và công ty.

# Mã lỗi

Bảng đầy đủ nằm ở [quy tắc phân bổ thanh toán](/domain/business-rules/payment-allocation-rules.md). Ví dụ phản hồi lỗi:

```json
{ "errors": { "allocations": ["payment_allocation_exceeds_invoice_balance"] } }
```

> Dạng JSON ở trên suy ra từ `ValidationException::withMessages`; cần xác nhận định dạng thực tế khi test.
