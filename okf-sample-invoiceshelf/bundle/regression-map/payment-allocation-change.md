---
type: Regression Map
title: Khi đổi phân bổ thanh toán thì phải test lại gì
description: Các vùng bị ảnh hưởng khi sửa PaymentAllocationService, công thức số dư hoặc thao tác phân bổ, kèm lý do và bằng chứng trong code.
tags: [regression, payment, allocation]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: alloc-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Receivables/Application/PaymentAllocationService.php
    title: PaymentAllocationService
  - id: balance-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/InvoiceBalanceService.php
    title: InvoiceBalanceService
---

# Phạm vi thay đổi

Sửa phân bổ thanh toán, `recalculate`, hoặc các màn hình/API tạo, sửa, xóa payment. Quy tắc gốc: [phân bổ](/domain/business-rules/payment-allocation-rules.md), [tính lại số dư](/domain/business-rules/balance-recalculation.md).

# Vùng bị ảnh hưởng

| # | Vùng | Vì sao bị ảnh hưởng | Cần test | Bằng chứng |
|---|---|---|---|---|
| 1 | Số dư và trạng thái hóa đơn | Phân bổ đổi `due_amount`, `status`, `paid_status`, xóa cờ `overdue` | Mọi chuyển trạng thái ở bảng trong quy tắc; cả hóa đơn cũ lẫn mới khi chuyển phân bổ | `InvoiceBalanceService::recalculate` |
| 2 | Thông báo nhân viên khi hóa đơn được trả đủ | Sự kiện `InvoicePaid` có listener | Chỉ phát khi **vừa** thành `PAID`, không phát cho credit note, không phát lại khi sửa phân bổ nhưng vẫn `PAID` | `NotifyStaff::invoicePaid` |
| 3 | Báo cáo thuế | Chỉ tính hóa đơn `paid_status = PAID` | Phân bổ làm hóa đơn thành/không thành `PAID` thì số trong báo cáo đổi | `Tax::scopeInvoicesBetween` |
| 4 | Khóa chỉnh sửa hóa đơn | `allow_edit` đọc `paid_status` | Hóa đơn bị khóa/mở khóa theo 3 chế độ `retrospective_edits` | `Invoice::getAllowEditAttribute` |
| 5 | Xóa hóa đơn | Hóa đơn có payment không xóa được | Xóa trước/sau khi bỏ phân bổ | `DeleteInvoiceRequest` |
| 6 | Credit note | Giới hạn credit phụ thuộc số đã thu | Credit khi đã thu một phần và đã thu đủ | `CreditNoteService::create` |
| 7 | Đổi trạng thái `COMPLETED` thủ công | Dựa trên tổng allocation và credit | Gọi `COMPLETED` khi còn dư và khi hết dư | `InvoiceService::changeStatus` |
| 8 | Quét quá hạn | Loại hóa đơn `COMPLETED` | Hóa đơn quá hạn rồi được trả đủ: `overdue` về false | `CheckInvoiceStatus`, `recalculate` |
| 9 | PDF biên nhận payment | Tạo PDF hoãn đến sau khi transaction commit | Không sinh PDF khi phân bổ bị từ chối | test "payment PDF generation is deferred..." |
| 10 | Ngoại tệ và `base_amount` | Chia `base_amount` theo tỷ lệ, dòng cuối nhận phần dư | Payment ngoại tệ chia nhiều hóa đơn; kiểm tra bất biến B3 | `PaymentAllocationService::baseAmounts`, `ForeignCurrencyAmountsTest` |
| 11 | Lệnh khôi phục liên kết cũ | Dùng chung service phân bổ | Chạy lệnh trên dữ liệu có liên kết không hợp lệ | `RestoreLegacyPaymentLinks` |
| 12 | Sao kê khách hàng, cổng khách hàng | Hiển thị số dư và lịch sử thanh toán | Số trên sao kê khớp `due_amount` | `CustomerStatementTest` (chưa đọc code, cần xác nhận) |

# Test tự động liên quan trong repo

`tests/Feature/PaymentAllocationTest.php`, `tests/Feature/CustomerStatementTest.php`, `tests/Feature/ForeignCurrencyAmountsTest.php`, `tests/Feature/DomainSpec/ReceivablesDomainTest.php`.
