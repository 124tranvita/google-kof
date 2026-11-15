---
type: Business Rule
title: Tính lại số dư hóa đơn
description: Công thức due_amount và cách status, paid_status được suy ra mỗi khi allocation hoặc credit note thay đổi.
tags: [invoice, balance, due-amount, status]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: balance-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/InvoiceBalanceService.php
    title: InvoiceBalanceService::recalculate
---

# Công thức

```
allocated = tổng amount của các allocation gắn với hóa đơn
credited  = - tổng total của các credit note gắn với hóa đơn   (dương)
due       = max(0, total - allocated - credited)
```

`due_amount = due` và `base_due_amount` là `due` quy đổi theo tỷ giá.[^balance-svc]

# Suy ra trạng thái

| Điều kiện | `status` | `paid_status` | `overdue` |
|---|---|---|---|
| `due = 0` | `COMPLETED` | `PAID` | đặt lại `false` |
| `due > 0` và `allocated > 0` | quay về trạng thái trước (`VIEWED` nếu đã xem, `SENT` nếu đã gửi, còn lại `DRAFT`) | `PARTIALLY_PAID` | giữ nguyên |
| `due > 0` và `allocated = 0` | như trên | `UNPAID` | giữ nguyên |

# Điểm đáng chú ý cho QA

* **Credit note một phần không làm hóa đơn thành `PARTIALLY_PAID`**, vì chỉ `allocated` quyết định. Hóa đơn chỉ được credit một phần (chưa có thanh toán) có `paid_status = UNPAID` dù `due_amount` đã giảm.
* Credit note toàn phần làm `due = 0`, nên hóa đơn thành `COMPLETED` và `PAID` dù không có tiền nào được thu.
* Sự kiện `InvoicePaid` chỉ được phát khi hóa đơn **vừa mới** chuyển sang `PAID`, không phải credit note, và `total > 0`. Sự kiện phát sau khi transaction commit.
* Người gọi hàm này phải giữ khóa hàng (row lock) của hóa đơn.

Hàm này được gọi từ [quy tắc phân bổ](payment-allocation-rules.md) và [quy tắc credit note](credit-note-rules.md). Xem [bản đồ hồi quy khi đổi phân bổ](/regression-map/payment-allocation-change.md).

[^balance-svc]: InvoiceBalanceService::recalculate
