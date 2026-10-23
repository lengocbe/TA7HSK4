# Lingo 1.8.0 · Bốn tập Khẩu ngữ bổ sung

Ngày giao: 17/10/2026. APK: `Lingo-SoTuVung-1.8.0.apk`, 91.284.785 byte (87,06 MiB).

## Nội dung

| Bộ sách | Bài | Từ/cụm từ | Mẫu câu |
| --- | --- | ---: | ---: |
| Cơ sở · Tập trên | 1–12 | 302 | 36 |
| Cơ sở · Tập dưới | 13–24 | 310 | 36 |
| Trung cấp | 1–14 | 491 | 42 |
| Nâng cao · 提高篇 | 1–20 | 658 | 60 |
| Tổng bổ sung | 58 | 1.761 | 174 |

Nội dung lấy từ bốn PDF được cung cấp, có chữ giản thể, pinyin, nghĩa tiếng Việt và trang nguồn. Mẫu câu là các câu/trích đoạn chọn từ bài khóa, không phải toàn bộ hội thoại. Bốn bộ xuất hiện cạnh hai tập Nhập môn trong Tiếng Hoa → Khẩu ngữ. Từng bài có tab Từ vựng và Mẫu câu giao tiếp; có giọng đọc tổng hợp đóng gói sẵn. Ví dụ phụ trên thẻ chưa có audio riêng.

Giữ nguyên 5.882 mục học, 200 nhóm bài và mọi MP3 của bản 1.7.0. Tổng app: 7.817 mục học/MP3, 258 nhóm bài. Kho từ, Tiến độ, Từ hay sai và ôn đến hạn lọc riêng từng bộ. Nguồn và các trường hợp số thứ tự in không liên tục được ghi trong `content/spoken-next/README.md`. Hạn chế tài liệu HSK 3 trước đây giữ nguyên.

## Kiểm tra

- Giao diện và dữ liệu: `test_app.py`, `test_bridge.py`, `test_mistakes.py`, `test_hsk23.py`, `test_hsk4.py`, `test_hsk5.py`, `test_hsk52.py`, `test_hsk6.py`, `test_spoken.py` đã đạt trong đợt phát triển này.
- `test_spoken_next.py`: kiểm tra 58 bài, thẻ học, đáp án cùng bộ và cùng loại mục, luyện lại câu sai, chống ghi sai hai lần, trạng thái nắm vững, nhập câu, ôn đến hạn, sao lưu/khôi phục, dữ liệu cũ và bố cục 320–700 px sáng/tối. Đạt trên APK và dữ liệu cuối.
- `test_assets.py`: kiểm tra byte/hash toàn bộ MP3, giải mã âm thanh không im lặng, CRC APK và mã giao diện/dữ liệu đóng gói. Đạt trên APK và dữ liệu cuối.
- `test_upgrade.py`: đạt trên APK cuối; cùng chứng thư ký với 1.0.0–1.7.0, versionCode 9, package `vn.lnb.sotuvung`, Android 8.0 trở lên, chữ ký và zip alignment hợp lệ.
- Không có thiết bị trong danh sách `adb devices`; chưa thử cài mới hoặc cài đè trên điện thoại thật. Kiểm tra trạng thái cài mới và khôi phục được thực hiện trong Chromium với bridge giả lập.

Các báo cáo máy đọc: `spoken-next-test-report.json`, `asset-test-report.json`, `upgrade-test-report.json`. Ảnh giao diện: `screenshots/spoken-next-courses.png`, `spoken-next-phrase.png`, `spoken-next-dark.png`.

## Dấu vết phát hành

SHA-256 APK: `9fc095184c831650ffc272752b7bfbb2fbc276b786e5d3d3d5308305edabccaf`

SHA-256 chứng thư ký: `86dc70cfc0ded65db1bf555547b2caa4d94e5df1415281456e44e1414ce69f4d`

Cài đè để giữ dữ liệu; không gỡ bản cũ. Hỗ trợ nhập sao lưu cũ. Chưa push repo và không tắt máy trong lần cập nhật này.
