---
type: Database Table
title: tax_types
description: "Định nghĩa loại thuế của công ty: cách tính, phía mua/bán, compound, mã EN 16931."
resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Models/TaxType.php
tags: [table, tax, tax-type]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: base-schema
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_01_01_000000_consolidate_base_schema.php
    title: Migration nền
  - id: en-mig
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/database/migrations/2026_10_24_120000_add_en16931_codes_to_tax_types_and_units.php
    title: Migration mã EN 16931
---

# Schema

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `name` | string | Duy nhất trong công ty (chỉ với loại `GENERAL`) |
| `calculation_type` | enum `percentage`/`fixed` | Mặc định `percentage` |
| `percent` | decimal(5,2), null | Dùng khi `percentage` |
| `fixed_amount` | integer, null | Dùng khi `fixed`, đơn vị minor |
| `compound_tax` | tinyint, mặc định 0 | Cộng dồn lên các thuế khác |
| `collective_tax` | tinyint, mặc định 0 | |
| `type` | enum `GENERAL`/`MODULE` | `MODULE` do module quản lý |
| `transaction_type` | string(20) | `sales` hoặc `purchases`. Dữ liệu cũ được xếp vào `sales` |
| `tax_category_code` | string(4), mặc định `S` | Mã EN 16931 (UNTDID 5305) |
| `tax_exemption_reason` | string(255), null | Lý do miễn thuế (BT-120) |
| `description`, `company_id` | | |

Xem [quy tắc loại thuế](/domain/business-rules/tax-type-rules.md) và [API loại thuế](/api/tax-types.md).
