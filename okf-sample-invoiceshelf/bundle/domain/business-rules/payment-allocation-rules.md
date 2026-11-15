---
type: Business Rule
title: Quy tắc phân bổ thanh toán
description: Điều kiện để một payment được phân bổ cho hóa đơn, mã lỗi tương ứng, tính nguyên tử và chia base_amount.
tags: [payment, allocation, validation, error-codes]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: alloc-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/Application/PaymentAllocationService.php
    title: PaymentAllocationService
  - id: alloc-test
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/tests/Feature/PaymentAllocationTest.php
    title: PaymentAllocationTest
---

# Điều kiện hợp lệ và mã lỗi

Mã lỗi trả về trong `errors.allocations` (hoặc `errors.amount`).[^alloc-svc]

| # | Điều kiện bị vi phạm | Mã lỗi |
|---|---|---|
| 1 | `invoice_id` trùng nhau trong cùng một yêu cầu | `payment_allocation_duplicate_invoice` |
| 2 | Thiếu `invoice_id`/`amount`, không phải số nguyên, `invoice_id < 1` hoặc `amount < 1` | `payment_allocation_invalid` |
| 3 | `payment.amount < 1` | `payment_amount_must_be_positive` (trên `amount`) |
| 4 | Tổng allocation lớn hơn `payment.amount` | `payment_allocation_exceeds_payment_amount` |
| 5 | Có `invoice_id` không tồn tại | `payment_allocation_invoice_not_found` |
| 6 | Hóa đơn khác **công ty**, **khách hàng** hoặc **tiền tệ** với payment | `payment_allocation_invoice_mismatch` |
| 7 | Hóa đơn là credit note, hoặc đang `DRAFT` | `payment_allocation_invoice_not_payable` |
| 8 | `amount` lớn hơn số còn có thể nhận | `payment_allocation_exceeds_invoice_balance` |

"Số còn có thể nhận" của một hóa đơn = `max(0, total - credited - tổng allocation từ các payment khác)`.

Với endpoint áp dụng tín dụng (xem [API phân bổ](/api/payment-allocations.md)):

| Điều kiện | Mã lỗi |
|---|---|
| Danh sách `allocations` rỗng | `payment_allocation_required` |
| Payment không thuộc công ty/khách hàng này | `payment_allocation_payment_not_found` |

# Hành vi

* **Thay thế toàn bộ** (`replace`): tập allocation mới thay hẳn tập cũ. Danh sách rỗng là hợp lệ (toàn bộ thành tín dụng chưa áp dụng).
* **Áp dụng tín dụng** (`applyCustomerCredits`): các dòng gửi lên được **cộng thêm** vào allocation hiện có, không xóa cái cũ.
* **Nguyên tử**: chạy trong một transaction; hóa đơn được khóa theo thứ tự id tăng dần để tránh deadlock và tránh hai yêu cầu cùng "tiêu" một số dư. Nếu bị từ chối, **không** có allocation nào thay đổi và `due_amount` giữ nguyên.[^alloc-test]
* Sau khi ghi, **mọi hóa đơn bị ảnh hưởng (cả cũ và mới)** được [tính lại số dư](balance-recalculation.md).
* **Chia `base_amount`**: chia theo tỷ lệ từ `base_amount` của payment, làm tròn xuống. Dòng cuối của payment được phân bổ hết nhận phần dư, để tổng `base_amount` các dòng bằng đúng `base_amount` của payment.

# Gợi ý TC

Mỗi dòng trong bảng lỗi trên là một TC âm tính. Xem [mẫu TC API](/testing/tc-templates/api.md) và [ví dụ TC tốt/tệ](/testing/good-vs-bad-tc.md).

[^alloc-svc]: PaymentAllocationService (normaliseAllocations, assertAllocationTotal, assertInvoiceCanReceiveAllocation, assertCreditRows, baseAmounts)
[^alloc-test]: PaymentAllocationTest, case "allocation over an invoice balance is rejected without changing allocations"
