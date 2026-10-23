# Nguồn HSK 6.1 / 6.2

Nguồn là hai PDF người dùng cung cấp: `Giáo trình chuẩn HSK6.1.pdf` (247 trang) và `Giáo trình chuẩn HSK6.2.pdf` (257 trang). Tài liệu là bản quét, được OCR để hỗ trợ nhập liệu; không đóng gói PDF vào app.

- `words.txt`: từng nhóm `#số_bài`, sau đó `chữ Hán|nghĩa tiếng Việt`. Sắp xếp khi build theo số bài. 6.1 có 922 mục, 6.2 có 1.041 mục.
- `examples.tsv`: `bài|các số từ|các trang PDF|trích đoạn tiếng Trung|bản dịch tiếng Việt`. Một trích đoạn có thể phục vụ nhiều từ. Tiêu đề/tiểu mục được gắn nhãn riêng trong dữ liệu đầu ra; các trích đoạn không nhất thiết là câu hoàn chỉnh.
- `provenance.json`: vị trí OCR của từng dòng từ mới, số thứ tự, trang PDF và cờ từ mở rộng. Chữ Hán đã hiệu chỉnh giữ riêng với văn bản OCR để có thể kiểm tra lại.
- `source-audit.json`: đầu ra đối chiếu từ và ví dụ do `scripts/build_hsk6.py` tạo.

Giữ đúng số thứ tự danh sách từ mới, kể cả phần tiếp theo ở trang thứ tư sau trang mở bài. Không lấy tên riêng ngoài danh sách này. Các lỗi nhận dạng chữ Hán đã được kiểm tra trên ảnh trang nguồn. Pinyin tạo bằng pypinyin, có hiệu chỉnh các từ đa âm và âm nhẹ theo ngữ cảnh; nghĩa và bản dịch tiếng Việt được biên soạn theo giáo trình. Phát âm là giọng tổng hợp, không phải bản ghi âm của sách.

Build lại dữ liệu bằng `python scripts/build_hsk6.py`; script chỉ thay nhóm level 6, giữ các bản ghi cũ. Không cần PDF hoặc OCR để build từ dữ liệu đã lưu. Để OCR lại nguồn phục vụ đối chiếu, dùng `scripts/extract_hsk6.py`; cache nằm trong `tmp/hsk6/`, không đưa vào Git. Nội dung trích phản ánh bối cảnh, quan điểm và số liệu trong giáo trình, không được cập nhật thành thông tin thời sự.
