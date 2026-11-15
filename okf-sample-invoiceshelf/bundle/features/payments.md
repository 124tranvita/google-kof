---
type: Feature
title: Ghi nhận và phân bổ thanh toán
description: Ghi nhận payment của khách, chia cho nhiều hóa đơn, giữ phần dư làm tín dụng và áp dụng tín dụng sau.
tags: [feature, payment, allocation]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: receivables-domain
    resource: https://github.com/InvoiceShelf/InvoiceShelf/tree/c8d10f7/app/Domains/Receivables
    title: Domain Receivables
---

# Mục đích

Thu tiền từ khách, gán cho hóa đơn, quản lý tín dụng chưa áp dụng, gửi mail/PDF biên nhận.

# Hub

| Khía cạnh | Xem |
|---|---|
| Thuật ngữ | [Payment allocation](/domain/glossary/payment-allocation.md) |
| Quy tắc | [Phân bổ thanh toán](/domain/business-rules/payment-allocation-rules.md), [Tính lại số dư](/domain/business-rules/balance-recalculation.md) |
| Dữ liệu | [customer_payment_allocations](/data/customer-payment-allocations.md) |
| API | [API phân bổ](/api/payment-allocations.md) |

# Test tự động hiện có (tham khảo)

`tests/Feature/PaymentAllocationTest.php` (đa hóa đơn, vượt số dư, sai tiền tệ/khách/draft/credit note, trùng, atomic, migration dữ liệu cũ), `tests/Feature/Receivables/PaymentComposerTest.php`, `tests/Unit/PaymentTest.php`.

# Test ngang

Xem [bản đồ hồi quy khi đổi phân bổ thanh toán](/regression-map/payment-allocation-change.md).
