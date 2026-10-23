# Lingo 1.7.0 · Khẩu ngữ Nhập môn

Ngày giao: 15/10/2026. APK: `Lingo-SoTuVung-1.7.0.apk` (64.95 MiB).

## Nội dung

| Tập | Bài | Từ/cụm từ | Mẫu câu |
| --- | --- | ---: | ---: |
| Nhập môn · Tập trên | 1–15 | 433 | 70 |
| Nhập môn · Tập dưới | 16–30 | 443 | 68 |
| Tổng bổ sung | 30 | 876 | 138 |

Lấy danh sách từ mới và các câu/trích đoạn bài khóa từ hai PDF đã cung cấp; có pinyin, nghĩa và bản dịch tiếng Việt, trang PDF nguồn. Bao gồm thành tố không đánh số được giải thích riêng, từ mở rộng (*) và từ lặp theo bài; không nhập danh sách tên riêng. Không phải toàn bộ hội thoại. Trong từng bài có tab Từ vựng/Mẫu câu giao tiếp với thẻ học và luyện tập riêng. Mỗi mục có giọng tổng hợp ngoại tuyến; một số từ đa âm dùng cụm ngắn có chú thích, ví dụ phụ không có audio riêng.

Giữ nguyên 4.868 bản ghi, 170 nhóm bài và mọi MP3 từ APK 1.6.0. Tổng hiện tại 5.882 mục học/MP3, 200 nhóm bài. Giới hạn tài liệu HSK 3 trước đây giữ nguyên, không thêm nội dung suy đoán.

## Kiểm tra

- `test_spoken.py`: đạt. Hai tập/30 bài, tab từ và câu, lựa chọn đáp án cùng loại và tập, luyện lại câu sai, tránh ghi sai hai lần, nắm vững giữ lịch sử, âm thanh qua bridge, lưu/khôi phục, trạng thái cài mới, ôn đến hạn, nhập câu và bố cục 320–700 px sáng/tối.
- `test_app.py`, `test_bridge.py`, `test_mistakes.py`, `test_hsk23.py`, `test_hsk4.py`, `test_hsk5.py`, `test_hsk52.py`, `test_hsk6.py`: đạt.
- `test_assets.py`: đạt. Toàn bộ 5.882 MP3 khớp hash, khớp byte trong APK, được đóng gói không nén; giải mã và có tín hiệu âm thanh. Mã giao diện và dữ liệu trong APK khớp workspace.
- `test_upgrade.py`: đạt. Cùng chứng thư ký với APK 1.0.0–1.6.0, chữ ký v2/v3 và zip alignment hợp lệ; package `vn.lnb.sotuvung`, versionCode 8, versionName 1.7.0, Android 8.0 trở lên.
- `test_android.py`: chưa chạy được bước cài vì không có máy ảo `emulator-5554`. Chưa thử trên điện thoại thật; kiểm tra trạng thái cài mới và khôi phục được thực hiện trong Chromium với bridge giả lập, không phải kiểm thử cài đặt Android thực tế.

Ảnh xem trước ở `screenshots/spoken-upper.png`, `spoken-lower.png`, `spoken-phrase.png`. Báo cáo máy đọc: `spoken-test-report.json`, `asset-test-report.json`, `upgrade-test-report.json`.

## Dấu vết phát hành

SHA-256 APK: `4291b9bad7f9227b331ff395882402cad7364f8bdc08008661a70b00e4ca809e`

SHA-256 chứng thư ký: `86dc70cfc0ded65db1bf555547b2caa4d94e5df1415281456e44e1414ce69f4d`

Công cụ tạo âm thanh cập nhật lên [edge-tts 7.3.1](https://github.com/rany2/edge-tts/releases/tag/7.3.1) sau lỗi kết nối của bản cũ. Việc tạo giọng chỉ xảy ra khi build; app không cần mạng khi học. Không thay âm thanh cũ.

Chưa push repo và không tắt máy trong lần cập nhật này.
