---
type: Glossary Term
title: Payment allocation (phân bổ thanh toán)
description: Một phần của khoản thanh toán được gán cho một hóa đơn cụ thể; phần chưa gán là tín dụng khách hàng chưa áp dụng.
tags: [glossary, payment, allocation]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: alloc-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/Application/PaymentAllocationService.php
    title: PaymentAllocationService
---

# Định nghĩa

Một khoản thanh toán (`Payment`) có thể được **chia cho nhiều hóa đơn**. Mỗi phần chia là một bản ghi trong [customer_payment_allocations](/data/customer-payment-allocations.md), có `amount` và `base_amount`.

* **Unapplied customer credit (tín dụng chưa áp dụng)**: phần tiền của payment chưa được phân bổ. Danh sách phân bổ rỗng vẫn hợp lệ và biểu diễn đúng trường hợp này.[^alloc-svc]
* Mỗi cặp (payment, invoice) chỉ có **một** dòng phân bổ (unique).
* Tiền đã phân bổ cho một hóa đơn là đầu vào của [tính lại số dư](../business-rules/balance-recalculation.md).

Quy tắc hợp lệ: xem [quy tắc phân bổ thanh toán](../business-rules/payment-allocation-rules.md).

[^alloc-svc]: PaymentAllocationService::replace docblock
