# Lingo 1.9.0 · New HSK Course / HSK 3.0

Ngày giao: 19/10/2026. APK: `Lingo-SoTuVung-1.9.0.apk`, 112,229,089 byte (107.03 MiB).

## Nội dung

| Bộ sách | Bài | Mục từ theo bài |
| --- | --- | ---: |
| HSK 3.0 · Cấp 1 | 1–15 | 330 |
| HSK 3.0 · Cấp 2 | 1–15 | 211 |
| HSK 3.0 · Cấp 3 | 1–18 | 483 |
| HSK 3.0 · Cấp 4 · Tập 1 | 1–10 | 392 |
| HSK 3.0 · Cấp 4 · Tập 2 | 11–20 | 407 |
| Tổng bổ sung | 68 | 1.823 |

Nhóm HSK 3.0 nằm cạnh HSK đang có và Khẩu ngữ. Từ và số bài lấy từ bảng từ cuối năm PDF được cung cấp, có chữ giản thể, pinyin, nghĩa tiếng Việt, trang nguồn và MP3 giọng tổng hợp ngoại tuyến. Bao gồm từ mở rộng (*) và các lần lặp theo bài; không nhập danh sách tên riêng. Thứ tự mục trong app theo bảng từ, không phải số thứ tự in trong từng phần bài khóa. Có 84 ví dụ trích tiêu đề được gắn nhãn; các mục khác chưa có câu ví dụ bài khóa và có thông báo rõ. Không trích toàn bộ hội thoại. Chi tiết và hiệu chỉnh nguồn ở `content/hsk30/README.md`.

Thẻ học, trắc nghiệm, Kho từ, ôn đến hạn, Tiến độ và Từ hay sai lọc riêng từng bộ. Giữ nguyên 7.817 mục học, 258 nhóm bài và mọi MP3 từ APK 1.8.0; không chuyển tiến độ giữa từ trùng chữ trong các bộ. Tổng app mới là 9.640 mục học/MP3 và 326 nhóm bài. Hỗ trợ sao lưu cũ; giới hạn PDF HSK 3 trước đây giữ nguyên.

## Kiểm tra

- `test_hsk30.py`: đạt. Năm bộ/68 bài, phân tách đáp án và lượt ôn, ghi sai một lần, luyện lại câu sai, nắm vững giữ lịch sử, nhập từ, âm thanh qua bridge, sao lưu/khôi phục, trạng thái cài mới, dữ liệu từ bản cũ và bố cục sáng/tối 320–700 px.
- `test_app.py`, `test_bridge.py`, `test_mistakes.py`, `test_hsk23.py`, `test_hsk4.py`, `test_hsk5.py`, `test_hsk52.py`, `test_hsk6.py`, `test_spoken.py`, `test_spoken_next.py`: đạt. Các kiểm tra giao diện dùng reduced motion để tránh chờ hiệu ứng; ứng dụng vẫn giữ hiệu ứng.
- `test_assets.py`: đạt. CRC APK, mã giao diện và dữ liệu đóng gói khớp workspace; tất cả 9.640 MP3 khớp hash/byte trong APK, được lưu không nén, giải mã được và có tín hiệu âm thanh.
- `test_upgrade.py`: đạt. Package `vn.lnb.sotuvung`, versionCode 10, versionName 1.9.0; chứng thư ký trùng các bản 1.0.0–1.8.0, chữ ký và zip alignment hợp lệ. Android tối thiểu 8.0.
- Không có thiết bị trong `adb devices`. Chưa thử cài mới/cài đè hoặc phát âm thanh trên điện thoại thật. Luồng cài mới và tiến độ được kiểm tra trong Chromium với bridge giả lập; tương thích cài đè được xác minh bằng metadata/chữ ký APK.

Ảnh giao diện ở `screenshots/hsk30-courses.png` và `screenshots/hsk30-dark.png`. Báo cáo máy đọc: `hsk30-test-report.json`, `asset-test-report.json`, `upgrade-test-report.json`.

## Dấu vết phát hành

SHA-256 APK: `a42cc8c83486627b3e5fd8819e4f6e289f77aa0e14c0d33fa6aefc038d880aab`

SHA-256 chứng thư ký: `86dc70cfc0ded65db1bf555547b2caa4d94e5df1415281456e44e1414ce69f4d`

Cài đè để giữ dữ liệu, không gỡ bản cũ. Chưa push repo và không tắt máy trong lần cập nhật này.
