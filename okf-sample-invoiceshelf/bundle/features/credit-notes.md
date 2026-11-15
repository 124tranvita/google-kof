---
type: Feature
title: Credit note
description: Tạo credit note toàn phần hoặc từng phần cho một hóa đơn và đồng bộ số dư.
tags: [feature, credit-note]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: credit-svc
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Application/CreditNoteService.php
    title: CreditNoteService
---

# Hub

| Khía cạnh | Xem |
|---|---|
| Thuật ngữ | [Credit note](/domain/glossary/credit-note.md) |
| Quy tắc | [Quy tắc credit note](/domain/business-rules/credit-note-rules.md), [Tính lại số dư](/domain/business-rules/balance-recalculation.md), [Khóa chỉnh sửa](/domain/business-rules/invoice-edit-lock.md) |
| API | [API credit note](/api/credit-notes.md) |
| Dữ liệu | [invoices](/data/invoices.md) |

# Test tự động hiện có (tham khảo)

`tests/Unit/CreditNoteAmountsTest.php` (tính tiền), `tests/Feature/DomainSpec/SalesDomainTest.php`.

# Test ngang

Xem [bản đồ hồi quy khi đổi credit note](/regression-map/credit-note-change.md).
