# HSK 5.2 theo giáo trình

18 bài từ 19 đến 36, gồm 665 mục trong danh sách từ mới, kể cả từ mở rộng (*). Không nhập danh sách tên riêng hoặc các bảng thuật ngữ mở rộng riêng biệt. File PDF người dùng cung cấp có 189 trang, trang PDF bằng số trang in + 1. Mã SHA-256 và số lượng từng bài ở `source-manifest.json`.

`words.txt` chứa từ theo thứ tự trong sách, loại từ và nghĩa Việt. `examples.tsv` ánh xạ bài / số từ / trang PDF / câu trích / bản dịch. `provenance.json` lưu trang của từng mục từ. `scripts/build_hsk52.py` tạo danh mục app, không cần PDF hoặc OCR để build lại.

Câu trích lấy từ nội dung sách, chỉnh dấu câu và lỗi OCR. Từ 情缘, 行动, 招儿 dùng tiêu đề bài, được gắn nhãn. Với từ tách rời 鼓掌 hoặc dạng láy 隐隐约约, trường exampleForms ghi dạng thực tế trong câu; không dùng các dạng này làm đáp án viết. Các mục trong ngoặc được hiển thị đầy đủ và chấp nhận dạng ngắn đúng sách khi luyện nhập. 鲇鱼 theo cách viết trong PDF và chấp nhận biến thể 鲶鱼.

Giữ nguyên các số liệu, câu chuyện và quan điểm trong bối cảnh giáo trình; các câu trích không phải thông tin cập nhật độc lập. Không đóng gói toàn bộ PDF vào APK.
