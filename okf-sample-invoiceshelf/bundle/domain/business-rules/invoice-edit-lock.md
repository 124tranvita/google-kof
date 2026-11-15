---
type: Business Rule
title: Khóa chỉnh sửa hóa đơn (retrospective_edits)
description: Khi nào một hóa đơn không còn được sửa, phụ thuộc credit note và cài đặt retrospective_edits của công ty.
tags: [invoice, edit, company-setting]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: invoice-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Models/Invoice.php
    title: Invoice::getAllowEditAttribute
---

# Quy tắc

Thuộc tính `allow_edit` của hóa đơn được tính như sau:[^invoice-model]

1. Hóa đơn **đã có credit note** thì **không bao giờ sửa được** (id dòng hàng của nó là mỏ neo cho các dòng của credit note).
2. Ngược lại, tùy cài đặt công ty `retrospective_edits`:

| Giá trị cài đặt | Không sửa được khi |
|---|---|
| `disable_on_invoice_sent` | `status` thuộc `DRAFT/SENT/VIEWED/COMPLETED` **và** `paid_status` là `PARTIALLY_PAID` hoặc `PAID` |
| `disable_on_invoice_partial_paid` | `paid_status` là `PARTIALLY_PAID` hoặc `PAID` |
| `disable_on_invoice_paid` | `paid_status` là `PAID` |
| giá trị khác / chưa đặt | luôn sửa được |

# Điểm cần xác nhận với dev

Danh sách `status` trong nhánh `disable_on_invoice_sent` gồm cả 4 giá trị, nên trên thực tế nhánh này **có vẻ cho kết quả giống** `disable_on_invoice_partial_paid`. Docblock của code mô tả "ba bước siết dần", nên nên hỏi lại hành vi mong đợi trước khi viết TC phân biệt hai chế độ này.

# Gợi ý TC

Ma trận 3 giá trị cài đặt × 3 giá trị `paid_status` × có/không credit note. Xem [thiết kế TC](/testing/test-design/money-and-rounding.md) về cách dựng dữ liệu.

[^invoice-model]: Invoice::getAllowEditAttribute (docblock và thân hàm)
