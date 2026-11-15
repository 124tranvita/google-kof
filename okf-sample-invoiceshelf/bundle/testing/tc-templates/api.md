---
type: Test Template
title: Template TC API
description: Cấu trúc chuẩn của TC API (request, mã trạng thái, body, kiểm tra DB), kèm ví dụ điền sẵn.
tags: [testing, template, api]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

# Cấu trúc

```markdown
## <ID> - <Hành động + điều kiện → kết quả>

| Mục | Nội dung |
|---|---|
| Loại / Ưu tiên | ... |
| Endpoint | <METHOD> <đường dẫn> |
| Quy tắc liên quan | <link concept> |
| Header | Authorization, company |

**Tiền điều kiện**: <dữ liệu cần có, kèm id>
**Request body**: <JSON đầy đủ>
**Kết quả mong đợi**
- HTTP status:
- Body (trường then chốt):
- DB sau khi gọi:
**Kiểm tra không tác dụng phụ** (TC âm tính)
```

# Ví dụ điền sẵn

## INV-ALLOC-API-001 - PUT allocations với tổng lớn hơn amount của payment bị từ chối

| Mục | Nội dung |
|---|---|
| Loại / Ưu tiên | Negative / P1 |
| Endpoint | `PUT /api/v1/payments/{payment}/allocations` ([API phân bổ](/api/payment-allocations.md)) |
| Quy tắc liên quan | [Quy tắc phân bổ](/domain/business-rules/payment-allocation-rules.md), dòng #4 |
| Header | `Authorization: Bearer <token>`, `company: <id công ty A>` |

**Tiền điều kiện**
- Hóa đơn I1 và I2 cùng công ty, cùng khách, cùng tiền tệ, `status = SENT`, mỗi hóa đơn `total = 100`.
- Payment P1 cùng khách và tiền tệ, `amount = 100`, chưa phân bổ.

**Request body**
```json
{ "allocations": [ { "invoice_id": <I1>, "amount": 60 }, { "invoice_id": <I2>, "amount": 50 } ] }
```

**Kết quả mong đợi**
- HTTP status: 422 (mặc định của Laravel với validation lỗi; xác nhận khi chạy).
- Body: lỗi chứa `payment_allocation_exceeds_payment_amount` ở trường `allocations`.
- DB: không có dòng nào trong `customer_payment_allocations` cho P1.

**Kiểm tra không tác dụng phụ**
- `due_amount` của I1 và I2 vẫn là 100; `paid_status` vẫn `UNPAID`.

# Biến thể nên sinh kèm

Một TC cho mỗi dòng mã lỗi trong bảng của quy tắc, và các TC thiếu trường, sai kiểu (`amount` = "abc", 0, -1), `allocations` không có mặt (vi phạm `present`), `invoice_id` trùng, header `company` của công ty khác.
