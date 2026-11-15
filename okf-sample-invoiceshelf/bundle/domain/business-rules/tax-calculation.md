---
type: Business Rule
title: Cách tính thuế và tổng tiền hóa đơn
description: Server tính lại sub_total, tax, total từ dòng hàng; quy tắc per-item, discount, compound và tax-inclusive, kèm ví dụ số.
tags: [tax, total, rounding, compound-tax]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: totals
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Support/DocumentTotals.php
    title: DocumentTotals
  - id: totals-test
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/tests/Unit/DocumentTotalsTest.php
    title: DocumentTotalsTest
---

# Nguyên tắc

Server **không tin** `total`, `sub_total`, `tax`, `due_amount` do client gửi (advisory GHSA-8c69). Chỉ tin giá, số lượng, giảm giá và **số tiền của từng dòng thuế**. Tổng được tính lại bằng `DocumentTotals::compute`.[^totals]

> Lưu ý cho QA: payload tạo hóa đơn vẫn **bắt buộc** các trường `total`, `sub_total`, `tax`. Giá trị gửi lên bị bỏ qua để tính lại, nhưng `amount` của từng dòng thuế do client gửi vẫn được dùng. Đây là điểm cần TC bảo mật/tamper.

# Công thức

```
item_total   = round(price × quantity) - item_discount        # item_discount chỉ áp dụng khi discount_per_item = YES
sub_total    = Σ item_total
sau_giảm     = sub_total - round(discount_val)                # giảm giá cấp tài liệu
thuế         = nếu tax_per_item = YES: thuế trên từng dòng (bỏ dòng thuế không có tax_type_id)
               ngược lại: thuế cấp tài liệu
               gồm nhóm simple và nhóm compound
tax          = simple + compound
total        = tax_included ? sau_giảm + compound : sau_giảm + tax
```

* `round` là làm tròn nửa ra xa số 0.
* Với `tax_included = true`, thuế simple đã nằm trong giá nên **không cộng thêm**, nhưng thuế **compound vẫn được cộng**.
* Số lượng âm được hỗ trợ.

# Ví dụ số (lấy từ unit test, đơn vị minor)

| # | Đầu vào | Kết quả |
|---|---|---|
| 1 | 1 dòng giá 10000 × 10, không thuế | `sub_total` 100000, `tax` 0, `total` 100000 |
| 2 | 1 dòng 1000 × 2; thuế tài liệu 150; giảm giá tài liệu 500 | `sub_total` 2000, `tax` 150, `total` 1650 |
| 3 | `tax_per_item = YES`; thuế dòng 100 và 200; thuế tài liệu 9999 | `sub_total` 3000, `tax` 300, `total` 3300 (thuế tài liệu bị bỏ qua) |
| 4 | Tax-included; giá 1000; thuế 100 | `total` 1000, `tax` 100 |
| 5 | Dòng 1000 × 2, `discount_val` 300; `discount_per_item` = YES / NO | `sub_total` 1700 / 2000 |
| 6 | Số lượng -2 × 100, 1 × 50, 0 × 75 | `sub_total` -150 |
| 7 | 10000; thuế 1900 và thuế compound 119 | `tax` 2019, `total` 12019 |

Các ví dụ trên lấy nguyên từ unit test.[^totals-test]

# Liên quan

* [Quy tắc loại thuế](tax-type-rules.md)
* [Credit note chia thuế theo tỷ lệ](credit-note-rules.md)
* [Thiết kế TC cho tiền và làm tròn](/testing/test-design/money-and-rounding.md)
* [Bản đồ hồi quy khi đổi thuế](/regression-map/tax-change.md)

[^totals]: DocumentTotals (docblock đầu class)
[^totals-test]: DocumentTotalsTest
