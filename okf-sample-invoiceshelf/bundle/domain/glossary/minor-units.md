---
type: Glossary Term
title: Minor units (đơn vị nhỏ nhất) và cột base_
description: Mọi số tiền lưu là số nguyên đơn vị nhỏ nhất (cent); mỗi cột tiền có cột base_ quy đổi sang tiền tệ của công ty.
tags: [glossary, money, rounding]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: invoice-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Models/Invoice.php
    title: Invoice model
  - id: changelog
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/CHANGELOG.md
    title: CHANGELOG
---

# Định nghĩa

* Số tiền là **số nguyên** đơn vị nhỏ nhất. Ví dụ `1000` nghĩa là 10.00 nếu tiền tệ có hai chữ số thập phân.[^invoice-model]
* Mỗi cột tiền có bản `base_` (ví dụ `base_total`, `base_due_amount`) bằng số tiền nhân tỷ giá của tài liệu, để công ty báo cáo bằng tiền tệ gốc mà không phải quy đổi lại.
* Chỉ hai giá trị là số thực: phần trăm giảm giá (`discount`) và tỷ giá (`exchange_rate`).
* Số tiền quy đổi sang tiền gốc được **làm tròn về cent nguyên trước khi lưu**, ở mọi nơi ghi (tài liệu, dòng hàng, thuế, bản sao, hóa đơn định kỳ, thanh toán, số dư). Tỷ giá vẫn giữ phần thập phân.[^changelog]

# Hệ quả cho QA

* Khi viết TC, luôn ghi cả giá trị hiển thị và giá trị lưu (ví dụ "10.00 (1000)").
* Cần TC cho ngoại tệ với tỷ giá có phần thập phân. Xem [thiết kế TC cho tiền và làm tròn](/testing/test-design/money-and-rounding.md).

[^invoice-model]: Invoice model (docblock)
[^changelog]: CHANGELOG, mục sửa lỗi PostgreSQL với tỷ giá có phần thập phân (#798, #862, #864)
