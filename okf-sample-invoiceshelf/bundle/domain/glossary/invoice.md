---
type: Glossary Term
title: Invoice (hóa đơn)
description: Tài liệu thanh toán lập cho khách hàng; một bảng chứa cả hóa đơn thường và credit note.
tags: [glossary, invoice]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: invoice-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Models/Invoice.php
    title: Invoice model
---

# Định nghĩa

Một bản ghi trong bảng `invoices`. Cột `type` phân biệt hai loại tài liệu:

| `type` | Ý nghĩa |
|---|---|
| `INVOICE` | Hóa đơn thường, số tiền dương |
| `CREDIT_NOTE` | Đảo ngược một hóa đơn, số tiền âm, có `related_invoice_id` trỏ về hóa đơn gốc. Xem [credit note](credit-note.md) |

Mỗi tài liệu có **hai trục trạng thái độc lập**:[^invoice-model]

* `status`: tiến độ gửi cho khách (`DRAFT`, `SENT`, `VIEWED`, `COMPLETED`).
* `paid_status`: tiền đã thu (`UNPAID`, `PARTIALLY_PAID`, `PAID`).

Hai trục này **không được set tay**, mà được suy ra lại mỗi khi số dư thay đổi. Chi tiết ở [mô hình trạng thái](../business-rules/invoice-state-model.md) và [tính lại số dư](../business-rules/balance-recalculation.md).

# Liên quan

* Tiền lưu theo [minor units](minor-units.md).
* Có dòng hàng (`invoice_items`) và thuế (`taxes`). Xem [cách tính thuế](../business-rules/tax-calculation.md).
* Dữ liệu: [bảng invoices](/data/invoices.md).

[^invoice-model]: Invoice model (docblock của class)
