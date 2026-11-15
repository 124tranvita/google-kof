# Thuật ngữ

* [Invoice (hóa đơn)](glossary/invoice.md) - một bảng, hai loại tài liệu, hai trục trạng thái
* [Credit note (hóa đơn điều chỉnh/hủy)](glossary/credit-note.md) - đảo ngược hóa đơn, số tiền âm
* [Payment allocation (phân bổ thanh toán)](glossary/payment-allocation.md) - chia một khoản thanh toán cho nhiều hóa đơn
* [Minor units (đơn vị nhỏ nhất)](glossary/minor-units.md) - tiền lưu dạng số nguyên, cột `base_`

# Quy tắc nghiệp vụ

* [Mô hình trạng thái hóa đơn](business-rules/invoice-state-model.md) - status, paid_status, overdue, xóa
* [Tính lại số dư](business-rules/balance-recalculation.md) - công thức due_amount
* [Quy tắc phân bổ thanh toán](business-rules/payment-allocation-rules.md) - điều kiện hợp lệ và mã lỗi
* [Quy tắc credit note](business-rules/credit-note-rules.md) - điều kiện, tính tiền từng phần
* [Cách tính thuế và tổng tiền](business-rules/tax-calculation.md) - exclusive/inclusive, compound, per-item
* [Quy tắc loại thuế](business-rules/tax-type-rules.md) - snapshot, xóa, mã EN 16931
* [Khóa chỉnh sửa hóa đơn](business-rules/invoice-edit-lock.md) - cài đặt retrospective_edits

# Luồng nghiệp vụ

* [Từ hóa đơn đến thu tiền](workflows/invoice-to-cash.md) - luồng end-to-end
