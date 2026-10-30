# Hán ngữ và Công sở — 1.11.0

Nguồn là bảy PDF do người dùng cung cấp trong X:/Han. Dấu vân tay nguồn nằm trong sources.json. Không đưa PDF nguyên bản vào APK.

| Khóa | Bài trong sách | Mục học |
|---|---|---:|
| Hán ngữ quyển 1 | 1–15 | 334 |
| Hán ngữ quyển 2 | 16–30 | 458 |
| Hán ngữ quyển 3 | 1–10 | 389 |
| Hán ngữ quyển 4 | 11–20 | 383 |
| Hán ngữ quyển 5 | 1–13 | 572 |
| Hán ngữ quyển 6 | 14–26 | 827 |
| Tiếng Trung công sở | 1–22 | 602 |

Quyển 1–4 là bản Giáo trình Hán ngữ cải tiến, quyển 5–6 là bản biên dịch khác của Tập III. Giữ số bài theo từng PDF, không gộp với HSK hoặc Khẩu ngữ. Tiêu đề Hán ngữ dùng số bài và quyển để tránh trộn tên bài giữa các ấn bản. Tên bài Công sở lấy từ mục lục.

Phạm vi trích xuất: phần từ mới và chỉ mục từ vựng, gồm từ thành phần, cụm/cấu trúc và tên riêng đọc được. Quyển 1 dùng chỉ mục PDF 164–175; quyển 2: 216–228; quyển 5: 186–196; quyển 6: 208–222. Quyển 3–4 và Công sở dùng bảng từ theo bài. Không coi số mục này là danh sách chuẩn HSK hay toàn bộ chữ xuất hiện trong sách.

Các PDF là bản quét. OCR được đối chiếu ở các dòng vỡ, chữ/phiên âm dính nhau và bảng chỉ mục. Nghĩa tiếng Việt chuẩn hóa dấu và điều chỉnh theo ngữ cảnh; overrides.json giữ các sửa chữa cụ thể, words.json lưu trang và dòng OCR gốc. Một số chữ nhiều cách đọc phát cụm ngắn có chú thích để xác định âm đọc. Đây là âm thanh tổng hợp, không phải audio gốc của giáo trình. Chưa có câu ví dụ/hội thoại cho các mục mới; thẻ học thông báo rõ.

## Tái tạo dữ liệu

Dữ liệu đầu vào đã biên tập được lưu trong words.json và lessons.json. Chạy scripts/build_han_office.py từ thư mục gốc; script chỉ thay dữ liệu của hai level han và office, không sửa bản ghi cũ. Sau đó chạy scripts/generate_audio.py, build:web và scripts/build_apk.py. scripts/extract_han_office.py tạo cache OCR phục vụ đối chiếu nếu có PDF nguồn.

source-audit.json ánh xạ mã từ phát hành sang dữ liệu nguồn; counts.json thống kê từng bài. tests/test_han_office.py kiểm tra nguồn, giữ nguyên bản 1.10.0, học/luyện sai/bộ lọc/khôi phục và bố cục màn hình. Chưa thử trên thiết bị Android thật.
