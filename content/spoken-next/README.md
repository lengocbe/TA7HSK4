# Bốn tập Khẩu ngữ bổ sung trong Lingo 1.8.0

| Khóa học | Bài chính | Từ/cụm từ | Mẫu câu chọn lọc |
| --- | --- | ---: | ---: |
| Cơ sở · Tập trên | 1–12 | 302 | 36 |
| Cơ sở · Tập dưới | 13–24 | 310 | 36 |
| Trung cấp | 1–14 | 491 | 42 |
| Nâng cao · 提高篇 | 1–20 | 658 | 60 |
| Tổng | 58 | 1.761 | 174 |

Nguồn là bốn PDF người dùng cung cấp: `03.汉语口语速成基础篇上.pdf`, `04_汉语口语速成基础篇下_c9f31dd8e7417dadc638df1bc09ce6fe.pdf`, `05_汉语口语速成中级篇_f6692daf032fa0179916f68392ff07ce.pdf`, `06_汉语口语速成提高篇_50896ca734943a56de0d741f5c71947e.pdf`. PDF gốc không được sửa hay đóng gói trong APK. Tên 提高篇 được giữ cạnh nhãn Nâng cao; nhãn này không quy đổi sang một cấp HSK. Bìa sách ghi tiếng Anh là Pre-intermediate.

`words.json` là bản chép từ mới đã rà soát, `phrases.tsv` chứa ba câu/trích đoạn bài khóa cho mỗi bài; không phải toàn bộ hội thoại. Nghĩa và bản dịch tiếng Việt được biên soạn theo ngữ cảnh. Mục từ thuộc danh sách từ mới được giữ theo bài, kể cả từ lặp giữa các bài. Năm món ăn ở bài 2 Cơ sở tập trên được đưa vào cùng bài. Không nhập các mục ôn tập phụ thành bài mới hay danh sách tên riêng riêng biệt; 淮河 được giữ vì được đánh số ngay trong danh sách từ mới của bài 11 Trung cấp.

Số thứ tự hiển thị trong app là thứ tự mục học, không phải luôn trùng số in trong sách: bài 11 Cơ sở tập trên nhảy từ số 2 sang 4 (PDF 120); bài 13 Trung cấp có hai số 18 (PDF 180). Giữ đủ các mục thực sự có trên trang, không tự thêm mục còn thiếu số. Hai mục 得 ở bài 10 được giữ riêng vì khác âm và nghĩa: děi (phải), dé (mắc bệnh).

`source-audit.json` giữ trang nguồn, OCR ban đầu, tọa độ và ghi chú sửa khi có. `overrides.json` ghi các hiệu chỉnh theo ngữ cảnh; các bảng `meanings*.tsv` ghi nghĩa bổ sung. Pinyin được tạo với từ điển và hiệu chỉnh chữ đa âm trong `scripts/build_spoken_next.py`. Các chữ đa âm cần cụm xác định có `speechText` và chú thích trong app.

Chạy lại catalog từ dữ liệu đã rà soát:

```powershell
python scripts/build_spoken_next.py
python scripts/generate_audio.py
pnpm build:web
python scripts/build_apk.py
python tests/test_spoken_next.py
```

OCR phục vụ đối chiếu, không tự ghi đè dữ liệu đã rà soát:

```powershell
python scripts/extract_spoken_next.py intermediate --source-dir "D:\LeNgocBE\Download\Telegram Desktop"
```

Mỗi mục từ và mẫu câu có MP3 giọng tổng hợp đóng gói sẵn. Những ví dụ phụ trên thẻ lấy từ câu đã chọn trong cùng bài, chưa có nút nghe riêng. Dữ liệu 1.7.0 được giữ nguyên, kể cả hạn chế tài liệu HSK 3 đã ghi ở bản trước.
