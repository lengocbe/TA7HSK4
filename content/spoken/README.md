# Hán ngữ khẩu ngữ cấp tốc · Nhập môn

Nguồn là hai bản PDF người dùng cung cấp (tập trên 179 trang, tập dưới 219 trang), tên file đầy đủ nằm trong `source-audit.json`. Trang nguồn là số trang PDF tính từ 1, không phải số in trên sách.

30 bài: tập trên bài 1–15, tập dưới bài 16–30. Có 876 mục từ/cụm từ từ danh sách từ mới (gồm từ mở rộng đánh dấu sao và các thành tố không đánh số được giải thích riêng), cùng 138 mẫu câu/trích đoạn chọn từ bài khóa. Không đưa danh sách tên riêng vào bộ từ. Từ lặp ở bài khác có mã riêng để giữ lịch ôn theo bài.

`words.json` là dữ liệu sau đối chiếu OCR và trang quét; `phrases.tsv` là các câu được chọn, có trang nguồn và bản dịch tiếng Việt. `meanings.tsv` và `overrides.json` ghi nghĩa và cách đọc theo ngữ cảnh. `lessons.tsv` ghi tiêu đề. `counts.json` ghi số lượng theo bài. `source-audit.json` nối mã từ ổn định với bản ghi nguồn, gồm dấu vết chỉnh lỗi OCR. `bookNumber` là thứ tự hiển thị trong app, không luôn trùng số in sách vì có thành tố không đánh số.

Chạy `python scripts/build_spoken.py` để cập nhật riêng mục Khẩu ngữ, giữ nguyên các mục khác. Script không cần PDF/OCR để build lại từ bộ dữ liệu đã duyệt. `scripts/extract_spoken.py` là bước OCR đọc nguồn, lưu kết quả tạm trong `tmp/spoken`; không thay thế việc đối chiếu thủ công.

Nghĩa và bản dịch tiếng Việt được biên soạn theo ngữ cảnh. Pinyin có chỉnh âm nhẹ, âm đa nghĩa và âm cuốn lưỡi trong mẫu câu. Các từ đa âm cần ngữ cảnh được đọc bằng cụm ngắn và có chú thích. Giọng đọc là giọng tổng hợp đóng gói MP3, không phải bản thu của nhà xuất bản. Mỗi từ/mẫu câu có audio riêng; ví dụ phụ chỉ hiển thị chữ. Chỉ thêm ví dụ khi có câu phù hợp trong các trích đoạn đã chọn, không tạo câu thay thế và không đưa toàn bộ hội thoại vào app.

Kiểm tra: `python tests/test_spoken.py`, `python tests/test_assets.py`, `python tests/test_upgrade.py` sau khi build APK. Không đóng gói PDF gốc vào ứng dụng.
