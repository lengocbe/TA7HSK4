# Boya trong Lingo 1.10.0

Sáu khóa riêng, chữ giản thể, pinyin, nghĩa tiếng Việt, trang PDF nguồn và MP3 ngoại tuyến. Không quy đổi các cấp Boya thành cấp HSK. Tên Sơ cấp / Trước trung cấp / Cao cấp theo sáu file người dùng gửi.

| Khóa | Bài | Mục |
|---|---:|---:|
| boya-1 · Sơ cấp tập 1 | 1–30 | 706 |
| boya-2 · Sơ cấp tập 2 | 1–25 | 792 |
| boya-3 · Trước trung cấp tập 1 | 1–16 | 492 |
| boya-4 · Trước trung cấp tập 2 | 1–16 | 765 |
| boya-5 · Cao cấp tập 1 | 1–10 | 794 |
| boya-6 · Cao cấp tập 2 | 1–10 | 605 |

Tổng 4.154 mục / 107 bài. Mục gồm từ, cụm từ, cấu trúc và một số tên riêng trong chỉ mục. Giữ từ lặp ở bài khác bằng mã riêng. Số hiển thị trong app là thứ tự nhập theo chỉ mục, không phải số thứ tự từ mới đã xác minh ở đầu bài. Các bài Boya chưa kèm câu ví dụ bài khóa; thẻ có thông báo rõ.

## Nguồn và giới hạn

Các PDF gốc ở thư mục người dùng cung cấp, không sửa và không đóng gói vào APK:

- `giao-trinh-boya-1.pdf`: chỉ mục PDF 231–241.
- `giao-trinh-boya-2.pdf`: chỉ mục PDF 178–189.
- `giao trinh boya_truoc trung cap_1.pdf`: chỉ mục PDF 242–257.
- `giao trinh boya truoc trung cap 2.pdf`: chỉ mục PDF 261–282.
- `giao-trinh-boya-cao-cap-1.pdf`: chỉ mục PDF 237–261.
- `giao-trinh-boya-cao-cap-2.pdf`: chỉ lấy mục đọc rõ từ bảng từ mới trong các bài; file có nhiều vùng chữ bị xô lệch, thiếu chữ và không có phần chỉ mục cuối sách được nêu trong mục lục.

**Cao cấp tập 2 là dữ liệu một phần, không phải toàn bộ từ vựng giáo trình.** Banner xuất hiện khi chọn tập và trong từng bài. `source-gaps.json` lưu các ứng viên bị loại do phần chữ hỏng; đây không phải thống kê đầy đủ mọi từ còn thiếu. Không đoán lại những mục không đọc rõ. Cần một bản PDF rõ hơn để bổ sung đầy đủ tập này.

Nghĩa tiếng Việt được biên dịch, có đối chiếu các từ đã có trong danh mục và điều chỉnh theo ngữ cảnh khi cần. Từ đa âm được rà; một số âm thanh dùng cụm ngắn có nhãn trong app. Không khẳng định bản phiên âm hoặc bản dịch là bản dịch chính thức của nhà xuất bản.

## Dữ liệu và tái tạo

- `lessons.tsv`: số bài, tiêu đề, trang bắt đầu để tham chiếu và bản dịch tiêu đề.
- `words.json`: dữ liệu đã duyệt, trang chỉ mục hoặc bảng từ mới.
- `manual.tsv`: các hàng được bổ sung sau khi xem ảnh trang, gồm 县 ở bài 9 được xác nhận thêm bằng bảng từ mới PDF 118–120.
- `overrides.json`: sửa OCR, nghĩa theo bài, cách đọc và cụm đọc.
- `meanings.tsv`: nghĩa tiếng Việt bổ sung.
- `source-audit.json`: nối từng mã từ với hàng nguồn; `source-files.json`: dấu kiểm tra PDF đầu vào.
- `counts.json`: số mục từng bài.

Chạy `python scripts/build_boya.py` để xây danh mục từ `words.json`, sau đó tạo audio và build như hướng dẫn trong README chính. `extract_boya.py` chỉ đọc PDF và tạo cache OCR; không tự thay dữ liệu đã duyệt. Mọi bản dựng phải giữ nguyên mã và nội dung 9.640 mục / 326 nhóm bài của 1.9.0 cùng từng MP3 cũ.
