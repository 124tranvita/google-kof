---
okf_version: "0.2"
---

# InvoiceShelf – QA Knowledge Bundle (mẫu)

Bundle mẫu về lát cắt **Hóa đơn – Thanh toán – Thuế** của InvoiceShelf 3.0.0-alpha.15 (commit `c8d10f7`, nhánh `3.x`). Mục đích: minh họa cách xây knowledge base cho QA bằng OKF v0.2. Mọi concept đều là bản nháp do AI sinh từ mã nguồn, **chưa có người duyệt** (`status: draft`, không có `verified`).

# Nghiệp vụ

* [Nghiệp vụ](domain/) - thuật ngữ, quy tắc nghiệp vụ, luồng end-to-end

# Chức năng, dữ liệu, API

* [Chức năng](features/) - mỗi chức năng một file, trỏ sang quy tắc, dữ liệu, API, TC
* [Dữ liệu](data/) - bảng DB liên quan và ý nghĩa cột
* [API](api/) - endpoint, payload, mã lỗi

# Kiểm thử

* [Kiểm thử](testing/) - template TC (Functional/API/UI), quy ước step, kỹ thuật thiết kế TC, ví dụ TC tốt/tệ
* [Bản đồ hồi quy](regression-map/) - "đổi X thì phải test lại Y"
* [Bài học từ bug](bugs/) - bug đáng nhớ và vùng ảnh hưởng

# Onboarding

* [Onboarding](onboarding/) - lộ trình đọc cho thành viên mới
