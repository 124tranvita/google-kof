---
type: Test Convention
title: Quy ước viết step và TC
description: "Quy tắc bắt buộc khi viết TC (người hoặc AI): đặt tên, đánh số, dữ liệu cụ thể, kết quả mong đợi, truy vết."
tags: [testing, convention, step]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

> Đây là **đề xuất khởi đầu** do AI soạn. Team cần thống nhất và chỉnh lại trước khi coi là chuẩn. Khi đã thống nhất, người có thẩm quyền ghi `verified: { by: human:<id>, at: ... }` vào frontmatter.

# Quy tắc chung (AI phải tuân thủ khi sinh TC)

1. **Một TC kiểm tra một điều.** Tiêu đề theo mẫu: `<Hành động> + <điều kiện> → <kết quả>`. Ví dụ: "Từ chối phân bổ khi số tiền vượt số dư hóa đơn".
2. **ID theo mẫu** `<MODULE>-<CHỨC NĂNG>-<số 3 chữ số>`, ví dụ `INV-ALLOC-003`.
3. **Mỗi step là một hành động** của một tác nhân. Bắt đầu bằng động từ: "Gọi", "Nhấn", "Nhập", "Chọn". Không gộp nhiều hành động vào một step.
4. **Dữ liệu cụ thể, không mô tả chung chung.** Viết "Số tiền: 1.01 (101)" thay vì "nhập số tiền lớn". Tiền luôn ghi **cả giá trị hiển thị và giá trị lưu** (xem [minor units](/domain/glossary/minor-units.md)).
5. **Kết quả mong đợi phải kiểm chứng được**: giá trị trường, mã lỗi, trạng thái, bản ghi DB. Cấm các cụm "hoạt động đúng", "hiển thị bình thường".
6. **Với TC âm tính, nêu rõ trạng thái KHÔNG đổi.** Ví dụ "Không có bản ghi allocation nào được tạo; `due_amount` vẫn 100".
7. **Tiền điều kiện mô tả trạng thái dữ liệu** (khách, tiền tệ, trạng thái hóa đơn, số dư), không chỉ "đã đăng nhập".
8. **Truy vết**: mỗi TC có dòng "Quy tắc liên quan" trỏ tới concept trong bundle (ví dụ [quy tắc phân bổ](/domain/business-rules/payment-allocation-rules.md)).
9. **Thuật ngữ nghiệp vụ** dùng đúng theo glossary, không tự đặt tên mới.
10. **Dữ liệu sau test**: ghi rõ cách dọn hoặc dùng dữ liệu độc lập, để TC chạy lại được.

# Danh sách kiểm tra cuối (AI tự rà trước khi nộp)

* [ ] Mỗi kết quả mong đợi có số liệu hoặc mã lỗi cụ thể?
* [ ] Có TC âm tính cho mỗi dòng mã lỗi trong quy tắc liên quan?
* [ ] Có TC biên (0, 1, giá trị ngay dưới/trên ngưỡng)?
* [ ] Có TC kiểm tra trạng thái không đổi khi bị từ chối?
* [ ] Các TC có độc lập, không phụ thuộc thứ tự chạy?

Xem [TC tốt và TC tệ](good-vs-bad-tc.md) để thấy cách áp dụng.
