---
type: Glossary Term
title: Credit note (hóa đơn điều chỉnh/hủy)
description: Tài liệu đảo ngược toàn bộ hoặc một phần hóa đơn, mang số tiền âm.
tags: [glossary, credit-note]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: credit-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/CreditNoteService.php
    title: CreditNoteService
---

# Định nghĩa

Một dòng trong `invoices` với `type = CREDIT_NOTE`, trỏ về hóa đơn gốc qua `related_invoice_id`. Mỗi dòng hàng của credit note có `source_invoice_item_id` trỏ về dòng hàng gốc mà nó đảo ngược.[^credit-svc] Mã code gọi là *Stornorechnung* trong comment.

Khác biệt chính với hóa đơn thường:

* Số tiền **âm**.
* Không nhận thanh toán. Xem [quy tắc phân bổ](../business-rules/payment-allocation-rules.md).
* Đánh số riêng theo cài đặt `credit_note_number_format`.
* Có thể credit **từng phần** theo số lượng của từng dòng. Xem [quy tắc credit note](../business-rules/credit-note-rules.md).

[^credit-svc]: CreditNoteService (docblock đầu class)
