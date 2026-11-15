---
type: Database Table
title: taxes
description: Thuế đã áp dụng lên một đối tượng (snapshot từ tax_types); số tiền có dấu.
resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Models/Tax.php
tags: [table, tax]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: base-schema
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_01_01_000000_consolidate_base_schema.php
    title: Migration nền
  - id: expense-mig
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_08_01_233036_add_expense_id_to_taxes_table.php
    title: Migration thêm expense_id
---

# Schema

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `tax_type_id` | int, bắt buộc | Loại thuế nguồn của snapshot. Không xóa được TaxType còn được tham chiếu |
| `invoice_id` / `invoice_item_id` | int, null | Thuế cấp hóa đơn hoặc cấp dòng |
| `estimate_id` / `estimate_item_id` / `item_id` / `recurring_invoice_id` / `expense_id` | int, null | Các chủ sở hữu khác |
| `name` | string | Tên chép từ TaxType lúc áp dụng |
| `percent` | decimal(5,2), null | Phần trăm chép từ TaxType |
| `compound_tax` | tinyint | Cờ compound chép từ TaxType |
| `amount` | bigint | Số tiền thuế, **có dấu** (credit note là số âm) |
| `base_amount` | bigint, null | Quy đổi sang tiền tệ công ty |
| `exchange_rate`, `currency_id` | | |

Model còn có `fixed_amount` và kiểu tính (`calculation_type`) được snapshot cùng.

# Quy tắc

* **Đúng một** cột chủ sở hữu được điền cho mỗi dòng.
* Báo cáo thuế cộng `base_amount` theo `tax_type_id`. Xem [quy tắc loại thuế](/domain/business-rules/tax-type-rules.md).
