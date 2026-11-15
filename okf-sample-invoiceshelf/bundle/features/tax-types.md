---
type: Feature
title: Loại thuế
description: Cấu hình loại thuế (phần trăm/cố định, compound, mua/bán, mã EN 16931) và ảnh hưởng lên chứng từ, báo cáo.
tags: [feature, tax, tax-type]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: taxation-domain
    resource: https://github.com/InvoiceShelf/InvoiceShelf/tree/c8d10f7/app/Domains/Taxation
    title: Domain Taxation
---

# Hub

| Khía cạnh | Xem |
|---|---|
| Quy tắc | [Loại thuế](/domain/business-rules/tax-type-rules.md), [Cách tính thuế](/domain/business-rules/tax-calculation.md) |
| Dữ liệu | [tax_types](/data/tax-types.md), [taxes](/data/taxes.md) |
| API | [API loại thuế](/api/tax-types.md) |

# Test tự động hiện có (tham khảo)

`tests/Feature/DomainSpec/TaxationDomainTest.php`, `tests/Unit/DocumentTaxesTest.php`, `tests/Unit/DocumentTotalsTest.php`.

# Test ngang

Xem [bản đồ hồi quy khi đổi thuế](/regression-map/tax-change.md).
