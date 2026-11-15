---
type: Feature
title: Quản lý hóa đơn
description: "Trung tâm điều hướng cho chức năng hóa đơn: quy tắc, dữ liệu, API, test hiện có và vùng cần test ngang."
tags: [feature, invoice]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: sales-domain
    resource: https://github.com/InvoiceShelf/InvoiceShelf/tree/c8d10f7/app/Domains/Sales
    title: Domain Sales
---

# Mục đích

Lập hóa đơn cho khách, gửi, theo dõi trạng thái thu tiền, nhân bản, chuyển từ/sang báo giá, hóa đơn định kỳ, nhắc nợ.

# Hub

| Khía cạnh | Xem |
|---|---|
| Thuật ngữ | [Invoice](/domain/glossary/invoice.md), [Minor units](/domain/glossary/minor-units.md) |
| Quy tắc | [Trạng thái](/domain/business-rules/invoice-state-model.md), [Tính lại số dư](/domain/business-rules/balance-recalculation.md), [Tính thuế](/domain/business-rules/tax-calculation.md), [Khóa chỉnh sửa](/domain/business-rules/invoice-edit-lock.md) |
| Dữ liệu | [invoices](/data/invoices.md), [taxes](/data/taxes.md) |
| API | [API hóa đơn](/api/invoices.md) |
| Luồng | [Từ hóa đơn đến thu tiền](/domain/workflows/invoice-to-cash.md) |

# Test tự động hiện có trong repo (tham khảo)

`tests/Unit/DocumentTotalsTest.php`, `tests/Unit/InvoiceTest.php`, `tests/Feature/DomainSpec/SalesDomainTest.php`, `tests/Feature/ForeignCurrencyAmountsTest.php`, `tests/Feature/Recurrence/RecurringInvoiceHardeningTest.php`.

# Test ngang khi thay đổi chức năng này

Xem [bản đồ hồi quy khi đổi thuế](/regression-map/tax-change.md) và [khi đổi phân bổ thanh toán](/regression-map/payment-allocation-change.md). Bổ sung: hóa đơn định kỳ, nhân bản, chuyển từ báo giá, PDF/mail, cổng khách hàng.
