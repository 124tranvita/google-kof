---
type: Regression Map
title: Khi đổi cách tính thuế hoặc loại thuế thì phải test lại gì
description: Các vùng bị ảnh hưởng khi sửa DocumentTotals, Tax, TaxType hoặc dữ liệu thuế của chứng từ.
tags: [regression, tax]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: totals
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Support/DocumentTotals.php
    title: DocumentTotals
  - id: tax-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Models/Tax.php
    title: Tax model
  - id: changelog
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/CHANGELOG.md
    title: CHANGELOG
---

# Phạm vi thay đổi

Sửa công thức tổng, cờ `tax_per_item`/`tax_included`/compound, thêm hoặc sửa TaxType, hoặc cách lưu `taxes`. Quy tắc gốc: [cách tính thuế](/domain/business-rules/tax-calculation.md), [loại thuế](/domain/business-rules/tax-type-rules.md).

# Vùng bị ảnh hưởng

| # | Vùng | Vì sao bị ảnh hưởng | Cần test | Bằng chứng |
|---|---|---|---|---|
| 1 | Tổng tiền hóa đơn | Server tính lại `sub_total`, `tax`, `total` | 7 ví dụ trong quy tắc; thêm tổ hợp cờ theo [ma trận](/testing/test-design/money-and-rounding.md) | `DocumentTotals`, `DocumentTotalsTest` |
| 2 | Báo giá, hóa đơn định kỳ | Cùng cơ chế tính tổng; `taxes` có cột chủ sở hữu riêng cho báo giá và hóa đơn định kỳ | Tạo và sửa báo giá/hóa đơn định kỳ với thuế per-item và compound | `taxes.estimate_id`, `taxes.recurring_invoice_id`; CHANGELOG nêu tính nhất quán cho hóa đơn định kỳ |
| 3 | Nhân bản, chuyển báo giá ↔ hóa đơn | Phải chép đúng thuế snapshot | So sánh tổng và từng dòng thuế giữa bản gốc và bản mới | `InvoicesController::clone`, `::convertToEstimate`, `EstimatesController::convertToInvoice` |
| 4 | Credit note | Chia thuế theo tỷ lệ từ `taxes.amount` đã lưu | Credit từng phần/toàn phần; hóa đơn credit đủ về 0 từng cent | `CreditNoteAmounts` |
| 5 | PDF, mail, trang công khai | Render đọc thuế của chứng từ | **Render nhiều lần liên tiếp cho cùng một chứng từ phải ra cùng một số** (xem [bài học bug](/bugs/tax-per-line-second-render-inflated.md)) | CHANGELOG #934 |
| 6 | Báo cáo thuế | Chỉ tính hóa đơn `PAID`; cộng `base_amount` theo `tax_type_id` | Tổng báo cáo khớp tổng thuế các hóa đơn đã trả trong kỳ; cả thuế cấp hóa đơn và cấp dòng | `Tax::scopeInvoicesBetween`, `scopeTaxAttributes` |
| 7 | Chi phí (purchases) | `taxes.expense_id`, TaxType có `transaction_type` | Thuế mua vào hiện đúng ở báo cáo; TaxType `sales` không lẫn `purchases` | `Tax::scopeExpensesBetween` |
| 8 | Xóa và sửa TaxType | Chặn xóa khi còn bản ghi `taxes`; sửa TaxType không đổi chứng từ cũ | Xóa loại thuế đã dùng (kỳ vọng 422 `taxes_attached`); sửa % rồi mở lại hóa đơn cũ | `TaxTypesController::destroy`, docblock `Tax` |
| 9 | E-invoice EN 16931 | TaxType có mã danh mục và lý do miễn thuế, module e-invoicing dùng | Loại thuế 0% phải đặt `Z` hoặc `E` kèm lý do; dữ liệu cũ mặc định `S` | CHANGELOG (alpha 13), `TaxType` |
| 10 | Cổng khách hàng | Có `TaxResource` riêng cho cổng | Số thuế khách thấy khớp phía quản trị | `Taxation/Http/Resources/CustomerPortal` |

# Test tự động liên quan trong repo

`tests/Unit/DocumentTotalsTest.php`, `tests/Unit/DocumentTaxesTest.php`, `tests/Unit/CreditNoteAmountsTest.php`, `tests/Feature/DomainSpec/TaxationDomainTest.php`.
