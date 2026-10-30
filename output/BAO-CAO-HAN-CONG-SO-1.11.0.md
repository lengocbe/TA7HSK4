# Lingo 1.11.0 — Hán ngữ và Công sở

APK: Lingo-SoTuVung-1.11.0.apk (200.856.630 byte, khoảng 192 MiB).

- Thêm Hán ngữ: 6 quyển, 76 bài, 2.963 mục từ/cụm từ.
- Thêm Công sở: 22 bài, 602 mục.
- Tổng bổ sung: 98 bài, 3.565 mục; tổng ứng dụng: 531 nhóm bài, 17.359 mục/MP3.
- Pinyin, nghĩa tiếng Việt, trang nguồn, audio tổng hợp ngoại tuyến; bộ lọc, ôn đến hạn và Từ hay sai riêng từng quyển.
- Giữ nguyên 13.794 bản ghi từ, 433 nhóm bài và file âm thanh của 1.10.0.

## Kiểm tra đã qua

- test_han_office.py: dữ liệu nguồn, ID, pinyin theo ngữ cảnh, hash audio, chọn từng khóa, trắc nghiệm các chế độ, chống ghi sai hai lần, luyện lại câu sai, đánh dấu đã nắm vững, khôi phục sao lưu và bố cục màn hình 320/390/700 px.
- test_boya.py, test_mistakes.py, test_app.py: kiểm tra hồi quy dữ liệu và chức năng cũ.
- test_bridge.py: mô phỏng cài mới, giao tiếp lưu/nạp và xuất/nhập sao lưu với Android.
- test_assets.py: CRC APK, tài nguyên đóng gói trùng workspace, toàn bộ 17.359 MP3 có hash khớp, giải mã được và có tín hiệu âm thanh.
- test_upgrade.py: cùng chứng chỉ với các APK 1.0.0–1.10.0, package vn.lnb.sotuvung, versionCode 12, Android tối thiểu 8.0, zip alignment hợp lệ.

## Cài đặt và giới hạn

Cài mới hoặc mở APK để cập nhật ứng dụng hiện có; không gỡ bản cũ trước khi cài đè. Nên xuất sao lưu trước khi cập nhật. Chưa cài thử trên điện thoại thật vì không có thiết bị kết nối; kiểm tra tương thích cài đè dựa trên metadata và chữ ký.

Các mục mới chưa có câu ví dụ/hội thoại. Từ vựng lấy từ bảng từ mới/chỉ mục của các bản quét, không phải toàn bộ nội dung sách. Một số từ đa âm phát cụm ngắn có chú thích. Boya Cao cấp tập 2 vẫn giữ giới hạn dữ liệu một phần đã công bố ở bản trước.

SHA-256: 204505c69e52c8ec31f6f081a9cc8a0cb2b051f043d7f05314e2415236f01212

Chưa push bản này lên repository; không thực hiện tắt máy.
