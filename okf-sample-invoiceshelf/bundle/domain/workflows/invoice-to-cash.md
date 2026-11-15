---
type: Workflow
title: Từ hóa đơn đến thu tiền
description: Luồng end-to-end tạo hóa đơn, gửi, thu tiền, phân bổ, credit note và đóng hóa đơn, kèm trạng thái tại mỗi bước.
tags: [workflow, invoice, payment]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: readme
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/README.md
    title: README
---

# Luồng chính

| Bước | Hành động | `status` | `paid_status` | Quy tắc áp dụng |
|---|---|---|---|---|
| 1 | Tạo hóa đơn (nháp) | `DRAFT` | `UNPAID` | [Cách tính tổng](../business-rules/tax-calculation.md) |
| 2 | Gửi cho khách | `SENT` | `UNPAID` | [Trạng thái](../business-rules/invoice-state-model.md) |
| 3 | Khách mở link | `VIEWED` | `UNPAID` | |
| 4 | Ghi nhận payment, phân bổ một phần | `VIEWED` | `PARTIALLY_PAID` | [Phân bổ](../business-rules/payment-allocation-rules.md), [Tính lại số dư](../business-rules/balance-recalculation.md) |
| 5 | Phân bổ phần còn lại | `COMPLETED` | `PAID` | phát sự kiện `InvoicePaid` |
| 6 | Quá hạn mà chưa đủ tiền | giữ nguyên | giữ nguyên | `overdue = true` bởi lệnh quét |

# Nhánh

* **Thu thừa**: phần chưa phân bổ là tín dụng khách hàng, áp dụng sau cho hóa đơn khác của cùng khách và cùng tiền tệ.
* **Credit note**: giảm số dư hóa đơn gốc, khóa chỉnh sửa. Xem [quy tắc credit note](../business-rules/credit-note-rules.md).
* **Hóa đơn định kỳ**: sinh hóa đơn theo lịch; có sự kiện `RecurringInvoiceGenerated` và `RecurringInvoiceFailed`.
* **Nhắc nợ**: có cài đặt nhắc thanh toán theo công ty và theo hóa đơn (`reminders_paused`).

> Các bước 1 đến 3 được suy ra từ hằng số trạng thái và lệnh trong code. Cần đối chiếu với màn hình thực để chắc chắn thứ tự.

# TC end-to-end nên có

Ít nhất một TC chạy suốt bước 1 đến 5 và kiểm tra trạng thái ở từng bước. Xem [mẫu TC chức năng](/testing/tc-templates/functional.md).
