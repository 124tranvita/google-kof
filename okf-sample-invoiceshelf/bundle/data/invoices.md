---
type: Database Table
title: invoices
description: Bảng chứa cả hóa đơn thường và credit note; ý nghĩa các cột quan trọng cho test.
resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_01_01_000000_consolidate_base_schema.php
tags: [table, invoice, credit-note]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: base-schema
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_01_01_000000_consolidate_base_schema.php
    title: Migration nền
  - id: credit-mig
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_08_02_120000_add_credit_note_support.php
    title: Migration thêm credit note
---

# Schema

Cột có trong migration nền hoặc migration credit note. Với các cột đánh dấu (*), mình đọc từ model/service và chưa đối chiếu vị trí migration, hãy xác nhận trên schema thật.

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `id` | increments | |
| `type` | string, mặc định `INVOICE` | `INVOICE` hoặc `CREDIT_NOTE` |
| `related_invoice_id` | int, null, index | Hóa đơn gốc của credit note |
| `credit_reason` | text, null | Lý do credit |
| `invoice_number` | string | Duy nhất theo công ty; credit note đánh số riêng |
| `invoice_date` | datetime | |
| `due_date` | date, null | Dùng cho [quét quá hạn](/domain/business-rules/invoice-state-model.md) |
| `status` | string | `DRAFT/SENT/VIEWED/COMPLETED` |
| `paid_status` | string | `UNPAID/PARTIALLY_PAID/PAID` |
| `overdue` | boolean, mặc định false | Cờ quá hạn |
| `sent`, `viewed` | boolean | Dùng để quay về trạng thái trước khi tính lại số dư |
| `tax_per_item`, `discount_per_item` | string `YES`/`NO` | Chế độ tính. Xem [cách tính thuế](/domain/business-rules/tax-calculation.md) |
| `tax_included`* | boolean | Giá đã gồm thuế |
| `discount`, `discount_type`, `discount_val` | decimal, string, bigint | Giảm giá cấp tài liệu |
| `sub_total`, `tax`, `total`, `due_amount` | bigint | [Minor units](/domain/glossary/minor-units.md); credit note mang giá trị âm |
| `base_discount_val`, `base_sub_total`, `base_tax`, `base_total`, `base_due_amount` | bigint, null | Quy đổi sang tiền tệ công ty |
| `exchange_rate` | decimal(19,6), null | Bắt buộc khi tiền tệ khác tiền tệ công ty |
| `currency_id`, `customer_id`, `company_id`, `creator_id`, `recurring_invoice_id` | khóa ngoại | |
| `sales_tax_type`, `sales_tax_address_type` | string, null | Kiểu thuế bán hàng |
| `unique_hash` | string | Link chia sẻ PDF (ai có hash đều xem được) |
| `reminders_paused`* | boolean | Tạm dừng nhắc nợ |

# Quan hệ

* `invoice_items` (cột `invoice_id`; dòng của credit note có `source_invoice_item_id`)
* [taxes](taxes.md) (thuế cấp hóa đơn)
* [customer_payment_allocations](customer-payment-allocations.md)
* credit notes: chính bảng này, `related_invoice_id`

# Ràng buộc nên kiểm tra

* `due_amount` phải bằng `max(0, total - Σ allocation - Σ credit)`. Xem [tính lại số dư](/domain/business-rules/balance-recalculation.md).
* Hóa đơn thường có `total >= 0`; credit note có tổng âm.
