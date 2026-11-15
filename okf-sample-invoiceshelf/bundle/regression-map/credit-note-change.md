---
type: Regression Map
title: Khi đổi credit note thì phải test lại gì
description: Các vùng bị ảnh hưởng khi sửa CreditNoteService, CreditNoteAmounts hoặc cách credit note liên kết với hóa đơn gốc.
tags: [regression, credit-note]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: credit-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/CreditNoteService.php
    title: CreditNoteService
  - id: invoice-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Models/Invoice.php
    title: Invoice model
---

# Phạm vi thay đổi

Sửa tạo credit note, công thức chia tiền, đánh số, xóa hoặc hiển thị credit note. Quy tắc gốc: [credit note](/domain/business-rules/credit-note-rules.md).

# Vùng bị ảnh hưởng

| # | Vùng | Vì sao bị ảnh hưởng | Cần test | Bằng chứng |
|---|---|---|---|---|
| 1 | Số dư và trạng thái hóa đơn gốc | Credit giảm `due_amount`; credit đủ đưa hóa đơn về `COMPLETED`/`PAID` | Credit một phần (vẫn `UNPAID`), credit đủ, credit sau khi đã thu một phần | `InvoiceBalanceService` |
| 2 | Khóa chỉnh sửa | Hóa đơn có credit note không sửa được | Sửa hóa đơn gốc trước và sau khi có credit note | `Invoice::getAllowEditAttribute` |
| 3 | Phân bổ thanh toán | Số còn có thể nhận trừ phần đã credit; credit note không nhận thanh toán | Phân bổ vào hóa đơn đã credit; phân bổ vào credit note (kỳ vọng `payment_allocation_invoice_not_payable`) | `PaymentAllocationService` |
| 4 | Đánh số | Credit note đánh số riêng theo `credit_note_number_format` | Số liên tục, không trùng với hóa đơn, không trùng khi tạo đồng thời | `CreditNoteService::persist` |
| 5 | Xóa hóa đơn | Phải xóa cùng credit note trong một batch | Xóa hóa đơn gốc không kèm credit note (bị từ chối); xóa cả hai | `CreditNoteDeletedTogether` |
| 6 | Thuế và `base_*` | Chia theo tỷ lệ từ giá trị đã lưu | Bất biến B6; hóa đơn ngoại tệ | `CreditNoteAmounts` |
| 7 | Mail, PDF, cổng khách hàng | Có `SendCreditNoteMail` và `CreditNoteResource` | Gửi mail credit note; số tiền hiển thị âm đúng định dạng | `Sales/Mail/SendCreditNoteMail.php` |
| 8 | Báo cáo | **Chưa khảo sát**: không rõ báo cáo doanh thu/thuế có cộng credit note âm hay không | Câu hỏi cần hỏi dev/BA, rồi viết TC | |
| 9 | Đồng thời | Khóa hàng hóa đơn gốc | Hai yêu cầu credit cùng lúc cho cùng một dòng | `CreditNoteService::create` |

# Test tự động liên quan trong repo

`tests/Unit/CreditNoteAmountsTest.php`, `tests/Feature/DomainSpec/SalesDomainTest.php`.
