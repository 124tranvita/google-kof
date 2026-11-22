# Tìm hiểu OKF (Open Knowledge Format) cho knowledge base của dự án QA

🇻🇳 Tiếng Việt · [🇬🇧 English](README.en.md)

Repo này gom tài liệu và bản mẫu để áp dụng **Open Knowledge Format v0.2** (Google Cloud) vào dự án SaaS về đăng ký chứng từ (denpyo) và quyết toán thuế.

## Nội dung

```
.
├── README.md                      # file này
└── okf-sample-invoiceshelf/       # bundle mẫu dựng từ dự án mã nguồn mở InvoiceShelf
    ├── HUONG-DAN.md               # hướng dẫn đọc bundle, ánh xạ sang dự án thật, giới hạn
    ├── GUIDE.en.md                # bản tiếng Anh của HUONG-DAN.md
    ├── tools/check_bundle.py      # script kiểm tra conformance, link, footnote
    ├── bundle/                    # Knowledge Bundle (35 concept, tiếng Việt, bản gốc)
    └── bundle-en/                 # bản dịch tiếng Anh của bundle (cùng cấu trúc)
```

## Nên đọc theo thứ tự

1. `okf-sample-invoiceshelf/HUONG-DAN.md`: cách bundle mẫu được làm và cách ánh xạ sang dự án của bạn.
2. `okf-sample-invoiceshelf/bundle/index.md`, rồi `domain/business-rules/balance-recalculation.md`, `testing/good-vs-bad-tc.md`, `regression-map/payment-allocation-change.md`.

## Tóm tắt nhanh về OKF

- Là **định dạng**, không phải công cụ: thư mục file Markdown có YAML frontmatter. Trường bắt buộc duy nhất là `type`.
- v0.2 thêm các trường nguồn gốc và độ tin cậy: `sources`, `generated`, `verified`, `status`, `stale_after`.
- `index.md` và `log.md` là tên dành riêng. Link nên dùng dạng tuyệt đối `/path/file.md` (tính từ gốc bundle).
- OKF **không** quy định cách tìm kiếm hay phục vụ. Có thể cho agent đọc trực tiếp thư mục, hoặc dựng RAG/MCP phía trên.
- Đọc file nào thì tốn token file đó. Dùng `index.md` để AI đọc dần từng lớp thay vì nạp cả bundle.

## Nhiều module trong một luồng nghiệp vụ

Spec không định nghĩa link giữa các bundle. Với ba module nối tiếp (đăng ký → duyệt → quyết toán thuế), nên dùng **một bundle, mỗi module một thư mục con**:

```
denpyo-knowledge/
├── index.md
├── shared/            # glossary, data, workflows/denpyo-end-to-end.md
├── registration/
├── approval/
├── tax-settlement/
├── testing/
└── regression-map/
```

Để AI truy vết được cả luồng, cần viết ra: concept luồng end-to-end, bảng bàn giao giữa module, link hai chiều kèm ngữ cảnh, và glossary/dữ liệu dùng chung. Link thiếu thì mạch đứt, nên cần quy trình duy trì.

## Kiểm tra bundle mẫu

```bash
cd okf-sample-invoiceshelf
python3 -I tools/check_bundle.py bundle
```

Lần chạy gần nhất: 35 concept, 0 lỗi. Cài `pyyaml` để parse YAML đầy đủ.

## Lưu ý

- Có bản tiếng Anh cho `README`, hướng dẫn (`GUIDE.en.md`) và bundle (`bundle-en/`). **Bản gốc là `bundle/` (tiếng Việt)**; khi sửa nội dung, sửa bản gốc trước rồi cập nhật `bundle-en/`. Hai bản chưa có công cụ tự đồng bộ.
- Bundle mẫu là **bản nháp do AI sinh từ mã nguồn, chưa ai duyệt** (`status: draft`, không có `verified`), và chưa chạy ứng dụng thật. Nó **không phải** knowledge của dự án bạn.
- Không đưa mã nguồn, DB hay spec của khách hàng vào công cụ AI bên ngoài khi chưa kiểm tra chính sách công ty. Không đưa dữ liệu thật vào bundle.

## Bước tiếp theo

- Dựng khung bundle cho dự án thật (denpyo): cần danh sách trạng thái denpyo qua ba module, 1–2 điểm bàn giao quan trọng, một TC khó hiểu do AI viết và một TC tốt.
- Chưa có thông tin thì để chỗ trống đánh dấu `<...>` rồi điền sau.
