# Lingo 1.10.0 · Bổ sung Boya

## Bản cài

- APK: `Lingo-SoTuVung-1.10.0.apk` · 159,898,823 byte (152.49 MiB).
- Package `vn.lnb.sotuvung`, versionCode **11**, Android 8.0 trở lên.
- SHA256 `7954ce39f7594d65c23b5ce6930b9eb5150880f0322ce5e742d1ce68700b15a2`.
- Cùng chứng chỉ ký với 1.0.0–1.9.0: `86dc70cfc0ded65db1bf555547b2caa4d94e5df1415281456e44e1414ce69f4d`.
- Cài mới hoặc cài đè. Không gỡ app cũ; nên xuất sao lưu trước khi cập nhật.

## Phần mới

Nhóm **Tiếng Hoa → Boya** có 6 khóa, tổng **4.154 mục / 107 bài**:

| Khóa | Bài | Mục |
|---|---:|---:|
| Sơ cấp tập 1 | 30 | 706 |
| Sơ cấp tập 2 | 25 | 792 |
| Trước trung cấp tập 1 | 16 | 492 |
| Trước trung cấp tập 2 | 16 | 765 |
| Cao cấp tập 1 | 10 | 794 |
| Cao cấp tập 2 · dữ liệu một phần | 10 | 605 |

Mục gồm từ, cụm từ, cấu trúc và một số tên riêng. Có pinyin, nghĩa tiếng Việt, trang PDF và giọng tổng hợp ngoại tuyến. Bộ lọc, Kho từ, tiến độ, ôn đến hạn, Từ hay sai và sao lưu dùng mã riêng từng tập. Nhóm giáo trình được xếp hai cột trên màn hình nhỏ để hiện đủ bốn nhóm.

## Giới hạn cần biết

**Cao cấp tập 2 chưa đầy đủ**: file người dùng gửi có nhiều vùng chữ xô lệch hoặc mất chữ và thiếu chỉ mục cuối sách. Chỉ nhập 605 mục đọc rõ từ bảng từ mới; app có thông báo tại tập và từng bài. Chưa thể bổ sung các mục còn lại nếu không có PDF rõ hơn. Không xem số ứng viên bị loại là tổng mọi từ bị thiếu.

Boya chưa có câu ví dụ bài khóa; thẻ có thông báo. Số thứ tự mục là thứ tự nhập theo chỉ mục, không phải số từ mới ở đầu bài. Nghĩa tiếng Việt được biên dịch và rà theo ngữ cảnh, không phải bản dịch chính thức của nhà xuất bản. PDF gốc không bị sửa và không nằm trong APK.

## Kiểm tra

- So sánh với APK 1.9.0: giữ nguyên từng trường của **9.640 mục / 326 nhóm bài** và từng MP3 cũ.
- Boya: 6 khóa, 107 bài, trang nguồn, các âm đa nghĩa đã chọn, dữ liệu mới tách khỏi HSK/Khẩu ngữ.
- Học mới, trắc nghiệm nghĩa/ngược/nghe/gõ, không ghi sai hai lần, luyện lại chỉ từ sai, đánh dấu nắm vững giữ lịch sử, ôn đến hạn tách khóa.
- Trạng thái trống tương đương lần đầu mở app; khôi phục sao lưu cũ, sao lưu mới và tải lại giữ tiến độ.
- Giao diện 320/360/390/700 px, sáng/tối, không tràn trang; mọi nút nhóm giáo trình đều hiển thị trọn.
- Kiểm tra các bộ HSK 2–6, HSK 3.0, Khẩu ngữ, luồng chung, lịch sử sai và giao tiếp cầu nối Android đều đạt.
- APK: ZIP CRC, mã web đúng bản hiện tại, **13.794 MP3** khớp manifest, giải mã được và không im lặng; MP3 đóng gói không nén.
- Chữ ký v2, package, versionCode tăng và zip alignment đạt.

**Chưa thử trên điện thoại thật.** Không có thiết bị ADB kết nối. Kiểm tra cài đè dựa trên metadata/chữ ký và kiểm tra nhập dữ liệu, không thay thế thử cài và nghe âm thanh trực tiếp trên thiết bị.

Chi tiết nguồn: `content/boya/README.md`, `source-audit.json`, `source-files.json`, `source-gaps.json`. Kết quả máy: `boya-test-report.json`, `asset-test-report.json`, `upgrade-test-report.json`.
