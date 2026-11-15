---
type: Bug Lesson
title: Render hóa đơn nhiều lần làm thuế từng dòng bị phồng
description: "Bug thật đã sửa ở InvoiceShelf 3.0 alpha 13: lần render thứ hai của cùng chứng từ có thuế theo dòng in ra số thuế bị tăng."
tags: [bug, tax, pdf, side-effect]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
sources:
  - id: changelog
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/CHANGELOG.md
    title: CHANGELOG (bản alpha 13, issue #934)
---

# Mô tả

Theo CHANGELOG: render một hóa đơn hoặc báo giá có **thuế theo dòng** từng làm thay đổi chính các dòng thuế mà nó đọc, nên lần render **thứ hai** của cùng chứng từ (ví dụ gửi mail sau khi đã tải về) in ra số thuế **bị phồng**. Đã sửa ở #934.[^changelog]

> Nguyên nhân chi tiết chưa được xác minh ở đây (không đọc diff). Phần dưới là bài học rút ra từ mô tả trong CHANGELOG.

# Bài học cho QA

* **Đọc không được làm thay đổi dữ liệu.** Mọi thao tác "chỉ xem" (render PDF, xem trước, tải về, gửi mail, mở link công khai, cổng khách hàng) đều cần TC lặp lại.
* Lỗi chỉ hiện ở **lần thứ hai**, nên TC chỉ chạy một lần sẽ bỏ sót.

# TC nên có (mẫu)

1. Tạo hóa đơn `tax_per_item = YES`, mỗi dòng một thuế phần trăm. Ghi lại tổng thuế T.
2. Tải PDF lần 1, sau đó tải lần 2, rồi gửi mail xem trước. Kỳ vọng: số thuế in ra giống nhau và bằng T ở cả ba lần.
3. Mở lại hóa đơn trên màn hình quản trị và qua cổng khách hàng: số thuế vẫn bằng T; bản ghi `taxes` trong DB không đổi.

# Vùng ảnh hưởng

[Khi đổi cách tính thuế](/regression-map/tax-change.md), dòng #5.

[^changelog]: CHANGELOG, mục sửa lỗi của bản alpha 13 (#934)
