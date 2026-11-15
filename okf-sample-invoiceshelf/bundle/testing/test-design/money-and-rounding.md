---
type: Test Design Guide
title: Thiết kế TC cho tiền, thuế và làm tròn
description: "Kỹ thuật thiết kế TC cho nghiệp vụ tiền: biên, làm tròn, bất biến cần kiểm tra sau mỗi thao tác, ma trận cờ, ngoại tệ, đồng thời."
tags: [testing, test-design, money, rounding, tax]
status: draft
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-14T16:00:00Z }
---

# 1. Bất biến: kiểm tra sau MỌI thao tác liên quan tiền

Nên viết thành bước "Kiểm tra bất biến" dùng chung (có thể là câu SQL hoặc gọi API đọc).

| # | Bất biến | Nguồn |
|---|---|---|
| B1 | `due_amount = max(0, total - Σ allocation - Σ credit)` | [Tính lại số dư](/domain/business-rules/balance-recalculation.md) |
| B2 | Σ allocation của một payment ≤ `payment.amount` | [Quy tắc phân bổ](/domain/business-rules/payment-allocation-rules.md) |
| B3 | Payment phân bổ hết: Σ `base_amount` các dòng = `payment.base_amount` | cùng nguồn |
| B4 | `due_amount = 0` ⇒ `status = COMPLETED` và `paid_status = PAID` | [Tính lại số dư](/domain/business-rules/balance-recalculation.md) |
| B5 | Credit note có tổng âm; Σ credit theo từng dòng ≤ số lượng dòng gốc | [Quy tắc credit note](/domain/business-rules/credit-note-rules.md) |
| B6 | Credit toàn bộ chia nhỏ (1+1+1) cho ra đúng từng trường như credit một lần | cùng nguồn |

# 2. Giá trị biên

* **Phân bổ**: số tiền = 0 (bị từ chối), 1, số dư − 1, **số dư**, số dư + 1.
* **Quá hạn**: `due_date` = hôm qua, **hôm nay** (chưa quá hạn), ngày mai. Xem [quá hạn](/domain/business-rules/invoice-state-model.md).
* **Credit**: số lượng = số lượng còn lại, còn lại + 0.01, và chuỗi nhiều lần credit tới khi hết.
* **Tổng tiền**: gần giới hạn `total` tối đa 999999999999 và vượt giới hạn.

# 3. Làm tròn

* Quy tắc: làm tròn **nửa ra xa số 0** (0.5 → 1, -0.5 → -1). Xem [cách tính tổng](/domain/business-rules/tax-calculation.md).
* Dữ liệu gợi ý: giá × số lượng thập phân cho kết quả có phần .5 (ví dụ số lượng 2.50), thuế phần trăm tạo phần lẻ, số lượng âm.
* Với credit từng phần, chọn dòng có số lượng 3 và tổng dòng **không chia hết cho 3** để lộ lỗi lệch cent. Kỳ vọng: tổng ba lần credit khớp đúng một lần credit hết (B6).

# 4. Ma trận cờ tính tiền

Các cờ ảnh hưởng công thức: `tax_per_item` (YES/NO), `discount_per_item` (YES/NO), `tax_included` (true/false), có thuế compound hay không. Đầy đủ là 16 tổ hợp; dùng **pairwise** để giảm, nhưng luôn giữ các tổ hợp sau:

* tất cả tắt (cơ sở);
* `tax_included = true` + compound (compound vẫn được cộng);
* `tax_per_item = YES` + thuế cấp tài liệu có giá trị (thuế cấp tài liệu bị bỏ qua);
* `discount_per_item = YES` + giảm giá cấp tài liệu cùng lúc.

# 5. Ngoại tệ

* Tỷ giá có phần thập phân (ví dụ 1.234567). Kiểm tra mọi cột `base_*` là số nguyên và nhất quán.
* Payment ngoại tệ phân bổ cho nhiều hóa đơn: kiểm tra B3 (dòng cuối nhận phần dư).
* Đổi tiền tệ công ty rồi cập nhật tỷ giá tài liệu cũ: từng số tiền phải được quy đổi từ chính giá trị của nó. CHANGELOG ghi một lỗi cũ ở đây (giảm giá bị lấy từ subtotal và thuế bị quy đổi hai lần, #862), nên đây là vùng dễ hồi quy.

# 6. Đồng thời

Hai yêu cầu cùng phân bổ hoặc cùng credit một hóa đơn. Kỳ vọng: hệ thống khóa hàng, chỉ một yêu cầu thành công nếu tổng vượt số dư, không bao giờ có `due_amount` âm hay tổng vượt hóa đơn.

# 7. Đa công ty và phân quyền

Mọi endpoint cần header `company`. Test chéo công ty: gọi với `company` của công ty B nhưng id hóa đơn của công ty A. Test vai trò (`owner`, preset Manager, Read only) cho từng thao tác ghi.
