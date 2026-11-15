---
type: Test Template
title: Template TC chức năng (Functional)
description: Cấu trúc chuẩn của một TC chức năng, kèm một ví dụ điền sẵn về phân bổ thanh toán.
tags: [testing, template, functional]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

# Cấu trúc

```markdown
## <ID> - <Hành động + điều kiện → kết quả>

| Mục | Nội dung |
|---|---|
| Loại | Positive / Negative / Boundary |
| Ưu tiên | P1 / P2 / P3 |
| Quy tắc liên quan | <link tới concept trong bundle> |

**Tiền điều kiện (trạng thái dữ liệu)**
- ...

**Dữ liệu test**
| Tên | Giá trị hiển thị | Giá trị lưu |

**Các bước**
1. <Động từ + đối tượng + dữ liệu>
2. ...

**Kết quả mong đợi**
- <kết quả kiểm chứng được: giá trị, mã lỗi, trạng thái, DB>

**Kiểm tra trạng thái sau test** (bắt buộc với TC âm tính)
- ...
```

Quy tắc điền xem [quy ước viết step](../step-conventions.md).

# Ví dụ điền sẵn

## INV-ALLOC-003 - Từ chối phân bổ khi số tiền vượt số dư hóa đơn

| Mục | Nội dung |
|---|---|
| Loại | Negative / Boundary |
| Ưu tiên | P1 |
| Quy tắc liên quan | [Quy tắc phân bổ thanh toán](/domain/business-rules/payment-allocation-rules.md), dòng #8 |

**Tiền điều kiện**
- Công ty A, khách hàng KH01, tiền tệ USD.
- Hóa đơn INV-0001: loại `INVOICE`, `status = SENT`, `total = 100`, `due_amount = 100`, chưa có allocation.
- Payment PAY-0001 của KH01, USD, `amount = 101`, chưa có allocation.

**Dữ liệu test**

| Tên | Giá trị hiển thị | Giá trị lưu |
|---|---|---|
| Số dư hóa đơn | 1.00 | 100 |
| Số tiền payment | 1.01 | 101 |
| Số tiền phân bổ | 1.01 | 101 |

**Các bước**
1. Mở PAY-0001 và chọn phân bổ cho hóa đơn INV-0001.
2. Nhập số tiền phân bổ 1.01 (101).
3. Lưu phân bổ.

**Kết quả mong đợi**
- Hệ thống từ chối với mã lỗi `payment_allocation_exceeds_invoice_balance`.

**Kiểm tra trạng thái sau test**
- Không có bản ghi nào trong `customer_payment_allocations` cho PAY-0001.
- INV-0001 vẫn `due_amount = 100`, `paid_status = UNPAID`.

> Ví dụ này bám theo test tự động hiện có trong repo ("allocation over an invoice balance is rejected without changing allocations"). Tên màn hình và nút ở các step 1 đến 3 cần thay bằng tên thật theo spec UI của dự án.
