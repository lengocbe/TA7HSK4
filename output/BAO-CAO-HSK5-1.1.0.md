# Bản cập nhật HSK 5.1 — Lingo 1.1.0

File cài: `Lingo-SoTuVung-1.1.0.apk` (13.177.615 byte, khoảng 12,6 MiB).

## Nội dung

- Mục HSK 5 riêng cạnh HSK 4 trong Bài học, Kho từ và Tiến độ.
- 18 bài, 723 mục từ mới theo thứ tự giáo trình HSK 5.1, bao gồm các mục mở rộng có dấu (*).
- Chữ giản thể, pinyin, loại từ, nghĩa tiếng Việt, trích dẫn trong sách và bản dịch; có trang nguồn cho từ và câu.
- Tổng cộng 1.137 file đọc từ ngoại tuyến. Một số chữ đa âm đơn lẻ được buộc đọc đúng bằng chữ đồng âm, có ghi trong manifest.
- Thẻ học, trắc nghiệm, nghe chọn từ, nhập chữ Hán, ôn đến hạn, từ yêu thích và sao lưu dùng được với HSK 5.
- Giữ nguyên 414 bản ghi từ cũ cùng ID; tiến độ HSK 4 và tiếng Anh được bảo toàn trong kiểm tra nâng cấp dữ liệu.

## Xác minh

- Build APK, chữ ký v2/v3, zip alignment: đạt.
- Cùng chứng thư ký với APK 1.0.0; cùng package `vn.lnb.sotuvung`, versionCode tăng lên 2: đạt.
- Luồng giao diện cũ và bridge Android giả lập: đạt.
- Phân cấp HSK 4/5, danh sách theo bài, học thẻ, đáp án cùng cấp, nhập dạng rút gọn, ôn đến hạn: đạt.
- Sao lưu cũ và khôi phục dữ liệu cả hai cấp: đạt.
- Giao diện sáng/tối, từ dài và câu dài trên màn hình 320/360/390/700 px: không tràn ngang trong các trường hợp kiểm tra.
- 1.137 MP3: khớp manifest và byte trong APK, không nén, giải mã được, có tín hiệu: đạt.
- Chưa thử cài/chạy trên điện thoại Android thật: `adb devices` không có thiết bị. Ảnh trong `screenshots/` là ảnh kiểm tra Chromium.

## Điểm cần biết

Sáu mục dùng tiêu đề bài làm trích dẫn và có nhãn rõ. Riêng 投篮 (bài 13) chưa tìm được câu ví dụ phù hợp trong phần bài đọc/bài tập đã rà; thẻ ghi chú cần đối chiếu. Không bổ sung câu tự viết. Pinyin và âm thanh đã kiểm tra kỹ thuật, chưa có người nghe rà toàn bộ từng bản ghi.

Bản dịch và câu trích phục vụ học ngôn ngữ, giữ bối cảnh thông tin trong giáo trình. Tập 5.2 và các bảng tên riêng/thuật ngữ tách riêng không thuộc bộ 723 mục này.

Cài APK đè lên bản 1.0.0 để cập nhật; không gỡ app cũ. Xuất bản sao lưu trong Cài đặt trước khi cập nhật. Xem `HUONG-DAN-CAI-DAT.md`.

Các báo cáo `*-test-report.json` ghi SHA-256 của đúng bản APK giao; mã băm cũng nằm trong `SHA256.txt`.
