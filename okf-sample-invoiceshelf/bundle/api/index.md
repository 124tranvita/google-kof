# API (tiền tố `/api/v1`, header `company`, xác thực Sanctum)

* [Hóa đơn](invoices.md) - CRUD, gửi, nhân bản, đổi trạng thái, xóa hàng loạt
* [Credit note](credit-notes.md) - `POST /invoices/{invoice}/credit-note`
* [Phân bổ thanh toán](payment-allocations.md) - thay thế phân bổ, áp dụng tín dụng
* [Loại thuế](tax-types.md) - CRUD tax-types
