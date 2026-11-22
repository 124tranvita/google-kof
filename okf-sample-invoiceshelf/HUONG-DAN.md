# Bundle OKF mẫu: InvoiceShelf (Hóa đơn – Thanh toán – Thuế)

Tiếng Việt · [English](GUIDE.en.md)

Thư mục này là ví dụ để bạn tham khảo cách dựng knowledge base theo **Open Knowledge Format v0.2** cho công việc QA. Nó **không phải** knowledge của dự án bạn.

```
okf-sample-invoiceshelf/
├── HUONG-DAN.md            # file này (nằm ngoài bundle)
├── tools/check_bundle.py   # script kiểm tra bundle theo spec
├── bundle-en/              # bản dịch tiếng Anh của bundle (cùng cấu trúc)
└── bundle/                 # ← đây mới là Knowledge Bundle gốc (35 concept)
    ├── index.md            # mục lục gốc, khai báo okf_version: "0.2"
    ├── log.md              # nhật ký thay đổi
    ├── domain/             # glossary, business-rules, workflows
    ├── features/           # mỗi chức năng một file "hub"
    ├── data/               # bảng DB
    ├── api/                # endpoint, payload, mã lỗi
    ├── testing/            # template TC, quy ước step, thiết kế TC, ví dụ tốt/tệ
    ├── regression-map/     # "đổi X thì phải test lại Y"
    ├── bugs/               # bài học từ bug thật
    └── onboarding/         # lộ trình đọc 5 ngày
```

**Nên đọc theo thứ tự:** `bundle/index.md` → `domain/business-rules/balance-recalculation.md` → `testing/good-vs-bad-tc.md` → `regression-map/payment-allocation-change.md`.

## 1. Vì sao chọn InvoiceShelf

Mã nguồn mở (Laravel + Vue), nghiệp vụ gần dự án của bạn: hóa đơn, thuế, thanh toán, credit note (hóa đơn điều chỉnh), báo cáo thuế. Có test tự động nên đối chiếu được. Bản mình dùng: **3.0.0-alpha.15, commit `c8d10f7`, nhánh `3.x`**. Đây là bản alpha, nên một số hành vi có thể đã đổi.

Mình chỉ làm **một lát cắt** (Hóa đơn – Phân bổ thanh toán – Credit note – Thuế), đủ để thấy toàn bộ cách làm.

## 2. Quy trình đã làm (bạn có thể lặp lại với dự án của mình)

1. **Đọc spec OKF gốc** (`SPEC.md` v0.2 trên GitHub) để biết trường nào bắt buộc, trường nào tùy chọn.
2. **Khảo sát code theo lát cắt**: model, service nghiệp vụ, request validation, route, migration, test.
3. **Rút ra thứ QA cần**: công thức, điều kiện hợp lệ, **mã lỗi**, giá trị biên, ràng buộc DB, quirk.
4. **Ghi mỗi thứ thành một concept**, trỏ `sources` về file code, dùng footnote để gắn nguồn cho từng khẳng định quan trọng.
5. **Nối bằng link**: chức năng ↔ quy tắc ↔ dữ liệu ↔ API ↔ test ↔ bản đồ hồi quy.
6. **Kiểm tra**: script kiểm tra conformance/link/footnote, và kiểm tra cú pháp YAML bằng công cụ riêng.

Với dự án thật, bước 2 và 3 làm cùng AI đọc source, DB và spec, rồi **BA/QA lead duyệt**.

## 3. Ánh xạ sang dự án của bạn (đăng ký chứng từ, quyết toán thuế)

| Trong bản mẫu | Trong dự án của bạn |
|---|---|
| `domain/glossary/` (invoice, credit note) | Thuật ngữ chứng từ, quyết toán, kỳ thuế, trạng thái đăng ký (JP–VN–EN) |
| `business-rules/tax-calculation.md` (công thức + 7 ví dụ số) | Quy tắc tính thuế, làm tròn, điều kiện đăng ký chứng từ, kèm ví dụ số lấy từ spec |
| `business-rules/payment-allocation-rules.md` (bảng mã lỗi) | Bảng điều kiện hợp lệ ↔ mã lỗi/thông báo của từng màn hình nhập |
| `data/*.md` | Bảng DB chính, ý nghĩa cột, khóa, ràng buộc |
| `testing/tc-templates/` + `step-conventions.md` | Chuyển các TC hiện có của bạn thành mẫu: chọn 5–10 TC **tốt nhất** làm chuẩn |
| `testing/good-vs-bad-tc.md` | Lấy một TC AI viết khó hiểu và bản bạn sửa lại |
| `regression-map/` | "Sửa chức năng A thì phải test B, C" lấy từ phụ thuộc trong code và lịch sử bug |
| `bugs/` | Bug đã gặp: nguyên nhân, vùng ảnh hưởng, TC phát hiện |
| `onboarding/` | Lộ trình đọc cho người mới |

Phần **giá trị nhất** với bạn là `business-rules` (nghiệp vụ thuế), `testing/` (khắc phục TC khó hiểu) và `regression-map/` (khắc phục việc khó test ngang).

## 4. Các tính năng OKF v0.2 được minh họa

| Tính năng | Ví dụ |
|---|---|
| `type` (bắt buộc), `title`, `description`, `tags` | mọi concept |
| `resource` (gắn với tài sản cụ thể) | `data/*.md` |
| `sources` + footnote gắn nguồn từng khẳng định | `domain/business-rules/credit-note-rules.md` |
| `generated` (ai/cái gì sinh ra nội dung) | mọi concept, `claude-code/claude-sonnet-5-5` |
| `verified` | **Cố ý không có**: chưa người nào duyệt, nên bundle ở mức "unverified" |
| `status: draft` | mọi concept; khi duyệt xong đổi thành `stable` |
| `stale_after` | các concept suy ra từ code: hết hạn sau 3 tháng, buộc phải rà lại |
| `index.md` ở từng thư mục (không frontmatter) | mọi thư mục |
| `okf_version` ở `index.md` gốc | `bundle/index.md` |
| `log.md` | `bundle/log.md` |
| Link tuyệt đối `/path/file.md` | khắp nơi |
| Khóa mở rộng tự đặt | `code_ref` (phiên bản code đã đọc) |

**Chưa dùng:** `Attested Computation` (concept mang cả công thức tính chuẩn kèm đoạn kiểm chứng để xác nhận AI đã chạy đúng công thức). Rất hợp để sau này ràng buộc "số thuế phải tính đúng công thức quy định", nhưng cần có executor và attester kèm theo, nên để giai đoạn sau.

## 5. Cách dùng với AI

Đưa bundle (hoặc các file liên quan) vào ngữ cảnh rồi yêu cầu, ví dụ:

* **Viết TC**: *"Dựa vào `domain/business-rules/payment-allocation-rules.md`, `testing/step-conventions.md` và `testing/tc-templates/api.md`, viết TC API cho mọi dòng trong bảng mã lỗi. Chỉ dùng mã lỗi và công thức trong tài liệu."*
* **Test ngang**: *"Tôi sắp sửa `PaymentAllocationService`. Dựa vào `regression-map/payment-allocation-change.md`, liệt kê 10 TC hồi quy ưu tiên cao nhất."*
* **Onboarding**: *"Giải thích cho người mới vì sao hóa đơn chỉ được credit một phần vẫn có `paid_status = UNPAID`, trích dẫn file nguồn."*

## 6. Giới hạn (nói thẳng)

* Mọi concept là **bản nháp do AI sinh từ mã nguồn, chưa ai duyệt**. Không dùng làm chuẩn kiểm thử khi chưa duyệt.
* **Chưa chạy ứng dụng.** Hành vi được suy ra từ đọc code và test; mục nào có chữ "cần xác nhận" nghĩa là chưa kiểm chứng thực tế.
* **Bản đồ hồi quy** dựa vào đọc code (nơi gọi hàm, listener, scope), chưa phải phân tích phụ thuộc đầy đủ. Còn dòng đánh dấu "chưa khảo sát".
* **Không có UI**: template TC UI để trống tên màn hình/nút.
* Phần `testing/` là **đề xuất khởi đầu** do AI soạn, team cần thống nhất.
* Spec OKF còn mới (v0.2), có thể đổi.

## 7. Vài phát hiện đáng chú ý khi khảo sát (để thấy giá trị của việc viết ra)

Đây là các điểm một TC viết vội thường bỏ sót. Tất cả cần xác nhận khi chạy thật:

1. Hóa đơn chỉ được **credit một phần** (chưa thu tiền) có `paid_status = UNPAID` dù số dư đã giảm; chỉ allocation mới đưa lên `PARTIALLY_PAID`.
2. `POST /invoices/{id}/status` với `SENT` gán `status = SENT` vô điều kiện, có vẻ hạ hóa đơn `VIEWED` về `SENT`.
3. `retrospective_edits`: hai chế độ `disable_on_invoice_sent` và `disable_on_invoice_partial_paid` có vẻ cho kết quả giống nhau.
4. `InvoicesController` không có `destroy`, nhưng route `DELETE /invoices/{invoice}` vẫn được đăng ký.
5. Sửa loại thuế bằng `PATCH` giữ nguyên tên bị báo trùng, còn `PUT` thì không.
6. Payload tạo hóa đơn bắt buộc `total/sub_total/tax` nhưng server tính lại; số tiền từng dòng thuế do client gửi thì vẫn được dùng.

## 8. Kiểm tra bundle

```bash
python3 -I tools/check_bundle.py bundle
```

Kiểm tra: mọi concept có `type`, `index.md` ngoài gốc không có frontmatter, footnote đã định nghĩa và khớp `sources[].id`, link nội bộ không hỏng. Cài `pyyaml` để script parse YAML đầy đủ. Lần chạy gần nhất: 35 concept, 0 lỗi, và bằng `js-yaml` cũng 0 lỗi cú pháp. Một bài học khi làm: `description` chứa dấu `: ` phải đặt trong ngoặc kép, nếu không YAML sai.

**Danh sách cần rà lại:**

```bash
python3 -I tools/check_bundle.py --review-list bundle
```

In các concept (1) chưa có `verified`, (2) có commit mới hơn lần `verified` cuối, (3) quá `stale_after`. Chỉ báo cáo, luôn thoát mã 0. So theo **ngày**, không theo giờ, vì commit ghi lại việc xác nhận luôn đến sau `verified.at`. Cần chạy trong repo git để lấy ngày commit.

## 9. Chỉnh sửa so với file trước

File `OKF-cho-du-an-QA.md` mình viết trước khi đọc spec gốc. Sau khi đọc, mình đã cập nhật: phiên bản hiện là **v0.2** (không phải v0.1), `timestamp` được thay bằng `generated.at`, danh sách nguồn là `sources` (không phải `source`), link nên dùng dạng tuyệt đối `/path.md`, và `index.md` / `log.md` là tên dành riêng.
