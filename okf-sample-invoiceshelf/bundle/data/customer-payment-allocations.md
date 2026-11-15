---
type: Database Table
title: customer_payment_allocations
description: Mỗi dòng gán một phần của một payment cho một hóa đơn; nguồn của tiền đã thu trên hóa đơn.
resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/Models/PaymentAllocation.php
tags: [table, payment, allocation]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: alloc-mig
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_08_02_230400_replace_payment_invoice_with_allocations.php
    title: Migration tạo bảng phân bổ
  - id: rename-mig
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_09_27_190911_rename_customer_payment_storage.php
    title: Migration đổi tên bảng payment
---

# Schema

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `id` | bigIncrements | |
| `payment_id` | unsigned bigint, index | Payment nguồn |
| `invoice_id` | unsigned int, index | Hóa đơn nhận |
| `amount` | unsigned bigint | Số tiền phân bổ (minor) |
| `base_amount` | unsigned bigint | Quy đổi sang tiền tệ công ty |
| `created_at`, `updated_at` | | |

* **Unique** `(payment_id, invoice_id)`.
* Bảng này vốn tên `payment_allocations`; bản 3.0 đổi thành `customer_payment_allocations` (và `payments` thành `customer_payments`). Module truy vấn bảng trực tiếp phải dùng tên mới.
* Bảng `legacy_payment_links` giữ các liên kết cũ không hợp lệ để khôi phục về tín dụng chưa áp dụng.

Xem [quy tắc phân bổ](/domain/business-rules/payment-allocation-rules.md).
