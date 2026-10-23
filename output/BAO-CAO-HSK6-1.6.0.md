# Lingo 1.6.0 — HSK 6.1 và HSK 6.2

Đã build APK: **Lingo-SoTuVung-1.6.0.apk**, 53.61 MiB.

## Nội dung mới

- HSK 6.1: bài 1–20, 922 mục từ.
- HSK 6.2: bài 21–40, 1.041 mục từ.
- Tổng thêm 1.963 mục từ theo số thứ tự từ mới trong hai PDF, kể cả mục mở rộng (*).
- Chữ giản thể, pinyin, nghĩa tiếng Việt, trích đoạn/tiêu đề trong giáo trình, bản dịch và trang nguồn.
- Giọng đọc tổng hợp ngoại tuyến từng từ; một số từ đa âm đọc trong cụm ngắn có chú thích. Chưa có giọng đọc câu ví dụ.
- Hai tập có bộ lọc riêng trong Bài học, Kho từ, Tiến độ, ôn đến hạn và Từ hay sai. Hàng chọn HSK 2–6 hiển thị đủ trên màn hình hẹp.

Toàn app có 4.868 mục từ, 170 nhóm bài học và 4.868 MP3. Giữ nguyên 2.905 bản ghi từ, các bài học và byte MP3 cũ từ APK 1.5.0. Từ trùng ở các bài vẫn có ID riêng để lưu tiến độ theo bài.

## Kiểm thử đã đạt

- `test_hsk6.py`: số bài/từ, số thứ tự và nguồn; dữ liệu cũ giữ nguyên; hai tập độc lập; lượt trắc nghiệm và ôn đến hạn không trộn tập; chống ghi sai hai lần; luyện lại chỉ từ sai; đã nắm vững giữ lịch sử và sai lại được đưa về cần luyện.
- Học thẻ, nhập chữ, nghe chọn đáp án và gọi giọng đọc qua bridge Android giả lập.
- Trạng thái cài mới trong Chromium; nhập sao lưu cũ; xuất/nhập lại; tải lại vẫn giữ bài học gần nhất của cả hai tập và tiến độ cũ.
- Giao diện sáng/tối, Bài học/Kho từ/Từ hay sai/thẻ chi tiết ở 320, 360, 390 và 700 px; nút chọn cấp không bị cắt.
- Các kiểm thử cũ: `test_app.py`, `test_bridge.py`, `test_hsk4.py`, `test_hsk5.py`, `test_hsk52.py`, `test_mistakes.py`, `test_hsk23.py`.
- `test_assets.py`: các file giao diện/dữ liệu trong APK khớp workspace; ZIP không lỗi; đủ 4.868 MP3 khớp hash, đóng gói không nén; tất cả giải mã được và có tín hiệu âm thanh.
- `test_upgrade.py`: package, versionCode, minSDK, căn chỉnh ZIP và chữ ký. Cùng chứng thư với APK 1.0.0–1.5.0.

## Cài đặt và giới hạn

Package: `vn.lnb.sotuvung`; versionCode **7**; versionName **1.6.0**; Android **8.0 trở lên**. Có thể cài mới hoặc cài đè theo kiểm tra package/chữ ký. Khi nâng cấp, xuất sao lưu trước và không gỡ bản cũ để giữ dữ liệu.

**Chưa kiểm thử trên điện thoại Android thật.** Kiểm thử luồng chạy trên Chromium với Android bridge giả lập; kiểm tra APK xác nhận metadata và chữ ký, chưa xác nhận cài đặt/cập nhật thực tế trên từng thiết bị. Các ảnh giao diện là ảnh Chromium.

Giới hạn nguồn HSK 3 của bản cũ không thay đổi: PDF thiếu trang sách 168–169; hai mục 万 và 嘴 có thông báo chưa có ví dụ đối chiếu. Nội dung HSK 6 dùng bản dịch biên soạn và trích đoạn theo bối cảnh giáo trình; âm thanh là giọng tổng hợp.

SHA-256 APK:
`30001eff05159f6477b47659d255e6838e3226205d3e099a930eb564c7b13345`

SHA-256 chứng thư ký:
`86dc70cfc0ded65db1bf555547b2caa4d94e5df1415281456e44e1414ce69f4d`
