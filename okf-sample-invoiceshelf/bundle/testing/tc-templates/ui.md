---
type: Test Template
title: Template TC UI
description: "Cấu trúc TC giao diện: màn hình, thao tác, thông báo, trạng thái hiển thị; phần tên nút/màn hình do dự án điền."
tags: [testing, template, ui]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

> Bundle mẫu này sinh từ mã nguồn backend nên **không có tên màn hình, nhãn nút thật**. Trong dự án thật, hãy điền các mục có dấu `[...]` từ spec UI hoặc ảnh chụp màn hình.

# Cấu trúc

```markdown
## <ID> - <Hành động + điều kiện → kết quả hiển thị>

| Mục | Nội dung |
|---|---|
| Loại / Ưu tiên | ... |
| Màn hình | [Tên màn hình theo spec] |
| Quy tắc liên quan | <link concept> |
| Trình duyệt / thiết bị | ... |

**Tiền điều kiện**: <tài khoản, vai trò, dữ liệu>
**Các bước**
1. Mở màn hình [tên màn hình].
2. Nhập [tên trường] = <giá trị cụ thể>.
3. Nhấn nút [nhãn nút].
**Kết quả mong đợi**
- Thông báo: "<nguyên văn thông báo>" (hiển thị tại [vị trí]).
- Trường/nhãn: <tên> hiển thị <giá trị cụ thể, định dạng tiền/ngày>.
- Trạng thái nút/trường: <bật/tắt/chỉ đọc>.
**Kiểm tra sau**: mở lại màn hình, dữ liệu vẫn đúng.
```

# Những thứ riêng của UI cần kiểm tra

* **Định dạng hiển thị** của tiền và ngày theo cài đặt công ty (ví dụ giá trị lưu `1000` hiển thị thành `10.00`). Xem [minor units](/domain/glossary/minor-units.md).
* **Nút bị khóa theo trạng thái**: chức năng sửa hóa đơn phụ thuộc [khóa chỉnh sửa](/domain/business-rules/invoice-edit-lock.md).
* **Thông báo lỗi**: backend trả **mã lỗi** (ví dụ `payment_allocation_exceeds_invoice_balance`); câu chữ người dùng thấy do bản dịch quyết định. TC UI nên ghi nguyên văn câu hiển thị cho từng ngôn ngữ cần test.
* **Cổng khách hàng** có màn hình riêng cho hóa đơn, báo giá và lịch sử thanh toán, cần TC phân quyền riêng.
