---
type: Business Rule
title: Quy tắc loại thuế (Tax Type)
description: Tax type định nghĩa cách tính thuế; Tax trên chứng từ là bản snapshot; ràng buộc xóa, trùng tên, mã EN 16931.
tags: [tax, tax-type, validation, en16931]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: taxtype-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Models/TaxType.php
    title: TaxType model
  - id: tax-model
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Models/Tax.php
    title: Tax model
  - id: taxtype-req
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Http/Requests/TaxTypeRequest.php
    title: TaxTypeRequest
  - id: taxtype-ctl
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Taxation/Http/Controllers/TaxTypesController.php
    title: TaxTypesController
---

# Hai khái niệm

* **TaxType** (`tax_types`): định nghĩa thuế của công ty. Cách tính là `percentage` hoặc `fixed`, thuộc phía `sales` hay `purchases`, có cộng dồn (`compound_tax`) hay không.[^taxtype-model]
* **Tax** (`taxes`): một thuế áp dụng cho một đối tượng. Là **bản snapshot**: tên, phần trăm, kiểu tính, số tiền cố định và cờ compound được chép từ TaxType lúc áp dụng, nên sửa TaxType về sau **không** làm đổi các chứng từ cũ.[^tax-model] Mỗi dòng `taxes` chỉ gắn với **một** đối tượng sở hữu (hóa đơn, dòng hóa đơn, hóa đơn định kỳ, chi phí hoặc mặt hàng catalog).

# Ràng buộc

| Quy tắc | Hành vi |
|---|---|
| Tên TaxType (loại `GENERAL`) là duy nhất trong công ty | Validation lỗi khi trùng |
| `calculation_type` bắt buộc, thuộc `percentage` hoặc `fixed` | |
| `transaction_type` thuộc `sales` hoặc `purchases` | |
| `tax_category_code` thuộc tập EN 16931: `S, Z, E, AE, K, G, O, L, M` | |
| `tax_exemption_reason` tối đa 255 ký tự | Các nhóm `E, AE, K, G, O` là nhóm đòi lý do miễn thuế theo quy tắc EN 16931 (BT-120); request hiện **không** ép bắt buộc nhập |
| Xóa TaxType đang được dùng | Bị từ chối: HTTP 422, `{"error": "taxes_attached"}`[^taxtype-ctl] |
| TaxType loại `MODULE` | Thuộc module, không hiện trong danh sách và không tham gia kiểm tra trùng tên |

# Quirk đã biết (để test cho đúng)

* Kiểm tra trùng tên **chỉ bỏ qua bản ghi đang sửa với method `PUT`**. Gửi `PATCH` với tên giữ nguyên sẽ bị báo trùng với chính nó.[^taxtype-req]
* Bộ lọc danh sách truyền `company_id` chỉ bật lọc; công ty thực tế lấy từ header `company`, không lấy từ giá trị gửi lên.

# Báo cáo thuế

Báo cáo thuế bán hàng chỉ tính các `Tax` thuộc **hóa đơn có `paid_status = PAID`** và `invoice_date` trong khoảng, cả thuế cấp hóa đơn lẫn thuế cấp dòng. Cần cả `from_date` và `to_date`, thiếu một đầu thì **không lọc**. Thuế chi phí lọc theo `expense_date` và không xét trạng thái thanh toán.[^tax-model]

Vì vậy mọi thay đổi làm đổi `paid_status` (xem [phân bổ thanh toán](payment-allocation-rules.md)) đều ảnh hưởng báo cáo thuế.

[^taxtype-model]: TaxType model (docblock)
[^tax-model]: Tax model (docblock và scope `scopeInvoicesBetween`)
[^taxtype-req]: TaxTypeRequest::rules (comment "Quirk kept as is")
[^taxtype-ctl]: TaxTypesController::destroy và helper respondJson (HTTP 422)
