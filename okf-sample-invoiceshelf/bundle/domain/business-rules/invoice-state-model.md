---
type: Business Rule
title: Mô hình trạng thái hóa đơn
description: Ý nghĩa và quy tắc chuyển của status, paid_status, overdue; đổi trạng thái thủ công, quá hạn và xóa.
tags: [invoice, status, overdue, delete]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: invoice-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/InvoiceService.php
    title: InvoiceService::changeStatus
  - id: overdue-cmd
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Console/CheckInvoiceStatus.php
    title: CheckInvoiceStatus command
  - id: delete-req
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Http/Requests/DeleteInvoiceRequest.php
    title: DeleteInvoiceRequest
---

# Các trục trạng thái

| Trục | Giá trị | Ai/cái gì đặt |
|---|---|---|
| `status` | `DRAFT`, `SENT`, `VIEWED`, `COMPLETED` | Gửi mail, khách mở link, [tính lại số dư](balance-recalculation.md), API đổi trạng thái |
| `paid_status` | `UNPAID`, `PARTIALLY_PAID`, `PAID` | Chỉ [tính lại số dư](balance-recalculation.md) |
| `overdue` (boolean) | true/false | Lệnh quét hằng ngày; tính lại số dư xóa cờ này khi đã trả đủ |

# Đổi trạng thái thủ công

API `POST /invoices/{invoice}/status` chỉ nhận `SENT` hoặc `COMPLETED`. Xem [API hóa đơn](/api/invoices.md).[^invoice-svc]

* `SENT`: đặt `status = SENT` và `sent = true`.
* `COMPLETED`: chỉ được khi số dư còn lại bằng 0 (tính từ allocations và credit notes) và `due_amount`, `base_due_amount` đều bằng 0. Nếu không, trả lỗi `invoice_must_be_settled_before_completion`.

> Điểm nên hỏi dev/BA khi test: nhánh `SENT` gán `status = SENT` vô điều kiện, nên một hóa đơn đang `VIEWED` có vẻ bị đưa về `SENT`. Chưa xác minh bằng chạy thật.

# Quét quá hạn

Lệnh `check:invoices:status` đánh dấu `overdue = true` khi hóa đơn thỏa **tất cả**:[^overdue-cmd]

* `type = INVOICE` (credit note không bao giờ quá hạn).
* `status` không phải `COMPLETED` hoặc `DRAFT`.
* `overdue` đang là false.
* `due_date` **nhỏ hơn** ngày hôm nay (so sánh theo ngày). Hóa đơn đến hạn đúng hôm nay **chưa** quá hạn.

Khi đánh dấu, hệ thống phát sự kiện `InvoiceBecameOverdue`.

# Xóa hóa đơn

API xóa hàng loạt `POST /invoices/delete` với danh sách `ids`. Mỗi id phải:[^delete-req]

* tồn tại trong `invoices`;
* **không có payment** nào gắn với nó (quan hệ `payments`);
* nếu có credit note trỏ về nó thì credit note đó phải **nằm cùng batch xóa**, nếu không bị từ chối.

[^invoice-svc]: InvoiceService::changeStatus
[^overdue-cmd]: CheckInvoiceStatus (docblock và handle)
[^delete-req]: DeleteInvoiceRequest::rules, các rule RelationNotExist và CreditNoteDeletedTogether
