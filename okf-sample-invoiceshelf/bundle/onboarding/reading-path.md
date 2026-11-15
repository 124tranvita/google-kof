---
type: Onboarding Guide
title: Lộ trình đọc 5 ngày cho QA mới
description: Thứ tự đọc bundle kèm bài tập thực hành mỗi ngày để thành viên mới nắm nghiệp vụ hóa đơn, thanh toán, thuế và cách viết TC.
tags: [onboarding, reading-path]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

> Lộ trình đề xuất, thời lượng là ước lượng. Người hướng dẫn nên chỉnh theo thực tế rồi mới đánh dấu đã duyệt.

# Ngày 1: Từ vựng và bức tranh tổng thể

1. [Invoice](/domain/glossary/invoice.md), [Credit note](/domain/glossary/credit-note.md), [Payment allocation](/domain/glossary/payment-allocation.md), [Minor units](/domain/glossary/minor-units.md).
2. [Từ hóa đơn đến thu tiền](/domain/workflows/invoice-to-cash.md).

**Bài tập**: vẽ lại luồng và tự điền `status`/`paid_status` ở từng bước, không nhìn tài liệu.

# Ngày 2: Trạng thái và số dư

1. [Mô hình trạng thái](/domain/business-rules/invoice-state-model.md).
2. [Tính lại số dư](/domain/business-rules/balance-recalculation.md).

**Bài tập**: cho hóa đơn total 300, payment 100 đã phân bổ và credit 50, tính `due_amount` và `paid_status`. Đáp án: `due_amount = 300 - 100 - 50 = 150`, `paid_status = PARTIALLY_PAID` (vì có phân bổ), `status` quay về trạng thái trước đó. Sau đó thử biến thể không có payment, chỉ credit 50, và giải thích vì sao `paid_status` là `UNPAID`.

# Ngày 3: Phân bổ và credit note

1. [Quy tắc phân bổ](/domain/business-rules/payment-allocation-rules.md).
2. [Quy tắc credit note](/domain/business-rules/credit-note-rules.md).

**Bài tập**: chọn 3 mã lỗi bất kỳ trong bảng, viết TC theo [mẫu API](/testing/tc-templates/api.md).

# Ngày 4: Thuế

1. [Cách tính thuế](/domain/business-rules/tax-calculation.md), [loại thuế](/domain/business-rules/tax-type-rules.md).
2. [Thiết kế TC cho tiền và làm tròn](/testing/test-design/money-and-rounding.md).

**Bài tập**: tự tính tay 3 ví dụ trong bảng, rồi tạo thêm 2 ví dụ có thuế compound và tax-included.

# Ngày 5: Viết TC đúng chuẩn và test ngang

1. [Quy ước viết step](/testing/step-conventions.md), [TC tốt và TC tệ](/testing/good-vs-bad-tc.md).
2. [Bản đồ hồi quy](/regression-map/) và [bài học bug](/bugs/tax-per-line-second-render-inflated.md).

**Bài tập**: giả sử "quy tắc phân bổ" thêm một điều kiện mới. Dùng bản đồ hồi quy liệt kê các vùng phải test lại và viết 5 TC ưu tiên cao nhất.
