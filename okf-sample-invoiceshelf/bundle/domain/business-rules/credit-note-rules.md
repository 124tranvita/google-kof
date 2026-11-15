---
type: Business Rule
title: Quy tắc credit note
description: Điều kiện tạo credit note toàn phần/từng phần, mã lỗi và nguyên tắc tính tiền để tổng các lần credit luôn khớp hóa đơn gốc.
tags: [credit-note, rounding, validation, error-codes]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: credit-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/CreditNoteService.php
    title: CreditNoteService
  - id: credit-calc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Support/CreditNoteAmounts.php
    title: CreditNoteAmounts
---

# Tạo credit note

Đầu vào: danh sách dòng cần credit `[{id, quantity}]` và `reason` (tùy chọn, tối đa 1000 ký tự). **Danh sách rỗng nghĩa là credit toàn bộ số lượng còn lại.**

| Điều kiện bị vi phạm | Mã lỗi |
|---|---|
| Không còn số lượng nào để credit, hoặc `total - đã thu - đã credit <= 0` | `invoice_already_fully_credited` |
| Số lượng credit lớn hơn số lượng đã xuất hóa đơn của dòng | `credit_quantity_exceeds_remaining` |
| Không dòng nào tăng so với lần credit trước | `credit_note_must_credit_something` |
| `đã credit + lần này > total - đã thu` | `credit_amount_exceeds_invoice_balance` |

Toàn bộ chạy trong transaction và **khóa hàng hóa đơn gốc** trước khi kiểm tra, vì hai credit đồng thời có thể cùng qua kiểm tra rồi vượt quá hóa đơn.[^credit-svc] Sau khi tạo, hóa đơn gốc được [tính lại số dư](balance-recalculation.md).

# Nguyên tắc tính tiền ("telescoping")

Credit của lần hiện tại = `cumulative(sau) - cumulative(trước)`, luôn tính từ **số liệu đã lưu của hóa đơn gốc**, không từ các credit note trước. Nhờ đó credit 3 đơn vị theo 1+1+1 ra đúng từng cent như credit 3 một lần, và hóa đơn credit đủ thì tổng về đúng 0.[^credit-calc]

* Số lượng xử lý theo **phần trăm** (2.50 là 250), không so sánh số thực.
* Làm tròn nửa ra xa số 0, cùng quy tắc với [cách tính tổng](tax-calculation.md).
* Dòng thuế **cố định** cũng được chia theo tỷ lệ (không tính nguyên một lần ở credit đầu tiên).
* Dòng thuế **phần trăm** chia theo `taxes.amount` **đã lưu**, không tính lại `percent × base`.
* Cột `base_*` chia theo `base_*` đã lưu của hóa đơn gốc, không nhân lại tỷ giá.

# Hệ quả

* Hóa đơn đã có credit note **không chỉnh sửa được** nữa. Xem [khóa chỉnh sửa](invoice-edit-lock.md).
* Credit note **không nhận thanh toán**. Xem [quy tắc phân bổ](payment-allocation-rules.md).
* Xóa hóa đơn gốc phải xóa kèm credit note. Xem [mô hình trạng thái](invoice-state-model.md).
* Credit note kế thừa cùng tiền tệ, kiểu thuế và kiểu giảm giá với hóa đơn gốc.

Xem [bản đồ hồi quy khi đổi credit note](/regression-map/credit-note-change.md).

[^credit-svc]: CreditNoteService::create và ::guard
[^credit-calc]: CreditNoteAmounts (docblock đầu class)
