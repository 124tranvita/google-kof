---
type: Test Example
title: Ví dụ TC tốt và TC tệ
description: So sánh một TC mơ hồ (kiểu AI thường sinh khi thiếu knowledge) với phiên bản dùng knowledge của bundle, có giải thích từng điểm.
tags: [testing, example, quality]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

# TC tệ

> **TC-045: Kiểm tra chức năng phân bổ thanh toán**
> 1. Vào màn hình thanh toán.
> 2. Nhập thông tin phân bổ.
> 3. Lưu.
>
> Kết quả mong đợi: Hệ thống hoạt động đúng.

## Vì sao tệ

| Vấn đề | Hậu quả |
|---|---|
| Tiêu đề chung chung, không nêu điều kiện | Không biết đang kiểm tra nhánh nào của [quy tắc](/domain/business-rules/payment-allocation-rules.md) |
| "Nhập thông tin" không có dữ liệu | Người mới không tái hiện được |
| Không có tiền điều kiện | Không biết cần hóa đơn trạng thái gì, số dư bao nhiêu |
| "Hoạt động đúng" không kiểm chứng được | Pass hay fail tùy cảm tính |
| Không nói trạng thái sau khi thao tác | Bỏ sót lỗi ghi dữ liệu dở dang |

# TC tốt (dùng knowledge của bundle)

Phiên bản đầy đủ nằm ở [mẫu TC chức năng](tc-templates/functional.md) (ID INV-ALLOC-003). Tóm tắt:

> **INV-ALLOC-003: Từ chối phân bổ khi số tiền vượt số dư hóa đơn**
> Tiền điều kiện: hóa đơn `SENT`, `due_amount = 100` (1.00); payment cùng khách, cùng tiền tệ, `amount = 101` (1.01).
> Bước: phân bổ 101 cho hóa đơn → Lưu.
> Kết quả: lỗi `payment_allocation_exceeds_invoice_balance`; không có dòng allocation nào được tạo; `due_amount` vẫn 100, `paid_status = UNPAID`.

## Vì sao tốt

* Gắn với **đúng một** dòng của bảng quy tắc, nên dễ truy vết khi quy tắc đổi.
* Có số liệu cụ thể cả dạng hiển thị lẫn dạng lưu.
* Kết quả là **mã lỗi và trạng thái DB** kiểm chứng được.
* Kiểm tra cả "không có tác dụng phụ", loại lỗi thường gặp nhất của nghiệp vụ tiền.

# Dùng cho AI

Khi yêu cầu AI sinh TC, đưa vào ngữ cảnh: [quy ước step](step-conventions.md), [mẫu TC](tc-templates/functional.md), quy tắc nghiệp vụ liên quan, và cặp ví dụ tốt/tệ này. Yêu cầu AI trích **mã lỗi và công thức từ quy tắc**, không tự suy diễn.
