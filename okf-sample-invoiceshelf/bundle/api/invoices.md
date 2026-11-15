---
type: API Endpoint
title: API hóa đơn
description: Các endpoint tạo, đọc, sửa, gửi, nhân bản, đổi trạng thái và xóa hóa đơn.
tags: [api, invoice]
status: draft
code_ref: c8d10f7
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
stale_after: 2027-02-14T00:00:00Z
sources:
  - id: routes
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/routes/company.php
    title: Sales routes
  - id: req
    resource: https://github.com/InvoiceShelf/InvoiceShelf/blob/c8d10f7/app/Domains/Sales/Http/Requests/InvoicesRequest.php
    title: InvoicesRequest
---

# Endpoint

Tiền tố `/api/v1`, cần header `company` và token Sanctum.[^routes]

| Method | Đường dẫn | Mục đích |
|---|---|---|
| GET, POST | `/invoices` | Danh sách, tạo |
| GET, PUT/PATCH | `/invoices/{invoice}` | Xem, sửa |
| POST | `/invoices/delete` | Xóa (hàng loạt) `{ids: [...]}`. Xem [quy tắc xóa](/domain/business-rules/invoice-state-model.md) |
| POST | `/invoices/{invoice}/status` | Đổi trạng thái, `status` thuộc `SENT` hoặc `COMPLETED` |
| POST | `/invoices/{invoice}/send` | Gửi mail; `GET .../send/preview` xem trước |
| POST | `/invoices/{invoice}/clone` | Nhân bản |
| POST | `/invoices/{invoice}/convert-to-estimate` | Chuyển thành báo giá |
| POST | `/invoices/{invoice}/credit-note` | Xem [API credit note](credit-notes.md) |
| GET | `/invoices/templates` | Danh sách template PDF |
| GET, POST, PUT | `/invoices/{invoice}/reminders` | Nhắc nợ theo hóa đơn |

# Payload tạo hóa đơn (rules chính)

| Trường | Quy tắc |
|---|---|
| `invoice_date` | bắt buộc |
| `customer_id` | bắt buộc |
| `invoice_number` | bắt buộc, **duy nhất** |
| `exchange_rate` | bắt buộc nếu ngoại tệ, ngược lại tùy chọn |
| `discount` | số, bắt buộc |
| `discount_val` | số nguyên, bắt buộc |
| `sub_total`, `tax` | bắt buộc (giá trị bị tính lại phía server) |
| `total` | số, bắt buộc, tối đa 999999999999 (tính lại phía server) |
| `template_name` | bắt buộc, phải là template tồn tại |
| `items` | bắt buộc, mảng; mỗi phần tử cần `name`, `quantity` (số), `price` (số) |

Xem [cách tính tổng](/domain/business-rules/tax-calculation.md) để hiểu vì sao `total` gửi lên không quyết định kết quả.

# Điểm cần xác nhận khi test

`Route::apiResources` đăng ký cả route `DELETE /invoices/{invoice}`, nhưng `InvoicesController` **không có phương thức `destroy`** (chỉ có `delete` cho `POST /invoices/delete`). Cần thử gọi route DELETE trên môi trường thật để biết kết quả (có thể là lỗi 500). Xóa hóa đơn nên đi qua `POST /invoices/delete` vì đó là nơi áp các rule kiểm tra.

# Mã lỗi nghiệp vụ

* `invoice_must_be_settled_before_completion` khi `COMPLETED` mà còn số dư.

[^routes]: Sales routes/company.php
