# Bản giao Lingo 1.0.0

Ngày: 07/10/2026, múi giờ Asia/Saigon.

**File cài Android:** `Lingo-SoTuVung-1.0.0.apk`, dung lượng khoảng 4,6 MiB. Yêu cầu Android 8.0 trở lên.

## Đã hoàn thành

- Trang chủ chọn Tiếng Anh / Tiếng Hoa và học tiếp bài gần nhất.
- 264 mục từ tiếng Anh theo 12 Unit Global Success 7, kèm 4 nhóm Review.
- 150 từ/cụm từ tiếng Hoa giản thể trong 10 bài chủ đề và 13 nhóm từ theo đề HSK 4.
- Phiên âm/pinyin, nghĩa tiếng Việt, loại từ, ví dụ và nguồn trang PDF.
- 414 MP3 đóng gói ngoại tuyến, giọng Anh Anh và tiếng phổ thông Trung Quốc; đọc thường/chậm.
- Thẻ học, ôn ngắt quãng, chọn nghĩa, chọn từ, nghe chọn từ, luyện nhập từ.
- Tìm kiếm, lưu từ, tiến độ bài/ngôn ngữ, mục tiêu ngày, chuỗi ngày học.
- Giao diện sáng/tối, lưu trên điện thoại và sao lưu/khôi phục JSON.
- APK có chữ ký phát hành; khóa ký giữ trong thư mục `signing/` của dự án để dùng cho cập nhật.

## Kết quả kiểm tra

| Hạng mục | Kết quả |
| --- | --- |
| Java, Dex, tài nguyên và đóng gói APK | Đạt |
| Chữ ký APK v2 và v3; căn chỉnh APK | Đạt |
| Kiểm tra luồng chức năng và lưu tiến độ trên Chromium | Đạt |
| Chiều ngang màn hình 320–700 px | Không tràn ngang trong các màn hình chính |
| Bridge UI/Android với dữ liệu mới cài và khôi phục | Đạt bằng mock |
| 414 âm thanh đúng byte/hash trong APK, không nén | Đạt |
| Giải mã MP3 và kiểm tra tín hiệu không im lặng | Đạt |
| Chạy trên Android/điện thoại thật | Chưa xác minh |

Bộ giả lập Android của máy tính lỗi khởi động QEMU ở cả bản 37.3.3 và 34.1.20 trong chế độ giả lập CPU phần mềm. App chưa được cài hoặc chạy trong máy ảo này, nên lỗi đó không phải kết quả chạy app. Script smoke Android được giữ ở `tests/test_android.py` để chạy khi có thiết bị kiểm tra thích hợp.

## Phạm vi nội dung

Tiếng Anh lấy bộ từ trọng tâm từ Glossary, chưa bao gồm mọi từ phụ trong tất cả bài đọc. Tiếng Hoa là bộ từ được chọn từ các đề, không phải toàn bộ danh mục HSK 4. Câu ví dụ chưa có âm thanh; chức năng thêm từ, đồng bộ và viết nét chữ chưa thuộc bản này. Kiểm tra âm thanh hiện là kiểm tra kỹ thuật; chưa có người nghe rà từng bản ghi.

Hướng dẫn cho người dùng: `HUONG-DAN-CAI-DAT.md`. Mã nguồn và hướng dẫn build: `../README.md`. Mã SHA-256 của APK: `SHA256.txt`.
