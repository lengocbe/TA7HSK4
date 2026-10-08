# Lingo · Sổ từ vựng Android

App Android học từ vựng tiếng Anh và tiếng Hoa, giao diện tiếng Việt, hoạt động ngoại tuyến. Bản cài: `output/Lingo-SoTuVung-1.0.0.apk`.

## Nội dung và tính năng

- Tiếng Anh: 264 mục từ trọng tâm theo Glossary của **Tiếng Anh 7 Global Success**, chia đúng 12 Unit, có 4 nhóm Review. Các mục đồng nghĩa ghi chung trong sách được tách để thuận tiện nghe và luyện.
- Tiếng Hoa giản thể: 150 từ/cụm từ chia 10 bài chủ đề, đối chiếu trên 13 PDF HSK 4. Có 13 bộ từ theo mã đề; tiến độ dùng chung với bài chủ đề.
- Mỗi từ có phiên âm/pinyin, loại từ, nghĩa tiếng Việt, ví dụ và nguồn. Ví dụ tiếng Anh được biên soạn bổ sung. Ví dụ tiếng Hoa lấy từ đề khi tìm được câu khớp; câu bổ sung ghi rõ “Ví dụ biên soạn”.
- 414 file MP3 phát âm từ, đóng gói trong APK, gồm giọng tổng hợp Anh Anh và tiếng phổ thông Trung Quốc. Không dùng giọng đọc cài trên điện thoại; không gọi dịch vụ mạng lúc học. Tốc độ bình thường hoặc chậm; hiện chưa có âm thanh cho câu ví dụ.
- Thẻ học, ẩn pinyin trước khi trả lời, bốn mức nhớ, chọn nghĩa, chọn từ theo nghĩa, nghe chọn từ, nhập từ tiếng Anh/chữ Hán.
- Lịch ôn: Quên sau 10 phút; Khó sau 1 ngày; Nhớ lần đầu 2 ngày rồi giãn khoảng hai lần; Dễ lần đầu 4 ngày rồi giãn khoảng ba lần; tối đa 365 ngày.
- Tìm kiếm bằng từ, nghĩa, IPA/pinyin; lưu từ yêu thích; tiến độ mỗi bài; mục tiêu ngày và chuỗi ngày học.
- Chế độ sáng/tối; sao lưu và khôi phục tiến độ qua file JSON.
- Không tài khoản, quảng cáo, quyền truy cập mạng, quyền microphone hoặc quyền lưu trữ rộng.

## Cài đặt

1. Chép APK vào điện thoại **Android 8.0 trở lên**.
2. Mở APK bằng ứng dụng quản lý file và cho phép ứng dụng đó cài đặt ứng dụng từ nguồn này nếu Android yêu cầu.
3. Cài rồi mở **Lingo • Sổ từ vựng**. Chọn Tiếng Anh hoặc Tiếng Hoa trên Trang chủ.
4. Chọn bài, nhấn Học từ mới. Bấm nút loa để nghe. Mở nghĩa rồi chọn mức độ nhớ để lưu lịch ôn.

Kho từ và Bài học có nút đổi ngôn ngữ. Bài học cho phép chọn mọi Unit/bài dù Trang chủ ưu tiên bài đã học gần nhất.

Android System WebView là bộ phận hiển thị có sẵn của Android. Mã giao diện đã được chuyển đổi để tương thích cú pháp với Chromium 60 trở lên; trên máy dùng WebView rất cũ, nên cập nhật WebView nếu giao diện hiển thị bất thường.

Để nhập chữ Hán khi luyện chính tả, dùng bàn phím tiếng Trung của điện thoại. Các bài chọn đáp án và thẻ học không yêu cầu bàn phím tiếng Trung.

## Dữ liệu và cập nhật

Tiến độ lưu riêng trên máy bằng Android SharedPreferences. Đóng/mở app vẫn giữ tiến độ. Gỡ app sẽ xóa dữ liệu app; xuất sao lưu trong Cài đặt trước khi gỡ hoặc đổi điện thoại. Khôi phục yêu cầu xác nhận và kiểm tra cấu trúc file trước khi thay dữ liệu.

Khóa ký phát hành và mật khẩu ở thư mục `signing/`, được loại khỏi Git. **Giữ nguyên thư mục này** và sao lưu riêng để bản cập nhật tiếp tục dùng cùng chữ ký. Không đưa khóa này lên kho mã công khai. APK đã ký có thể gửi đến điện thoại; không cần gửi thư mục signing.

## Mã nguồn

| Đường dẫn | Vai trò |
| --- | --- |
| `android/` | Activity Android, MediaPlayer, lưu tiến độ và chọn file sao lưu |
| `www/app.js` | Logic giao diện, thẻ học, bài luyện và ôn ngắt quãng |
| `www/app.compat.js` | Bản chuyển đổi tương thích dùng trong APK |
| `www/style.css` | Giao diện điện thoại, sáng/tối |
| `www/audio/` | 414 file MP3 ngoại tuyến |
| `content/english.tsv` | Nội dung tiếng Anh đã đối chiếu Glossary |
| `content/chinese.tsv` | Nội dung tiếng Hoa theo chủ đề |
| `content/catalog.json` | Dữ liệu bài học và nguồn trang PDF |
| `content/audio-manifest.json` | Văn bản, giọng, kích thước và hash của mỗi MP3 |
| `scripts/` | Chuẩn bị SDK, dữ liệu, âm thanh và build APK |
| `tests/` | Kiểm tra các luồng học, dữ liệu và âm thanh đóng gói |
| `output/` | APK, hướng dẫn và báo cáo kiểm tra |

## Build lại

Môi trường: Windows, Python 3.12+, Node.js, pnpm và JDK 17+. Máy hiện dùng JDK 23. Script build trực tiếp bằng SDK 35, không cần Android Studio hay Gradle. `JAVA_HOME` có thể dùng để chọn JDK khác.

```powershell
python -m pip install -r requirements-build.txt
pnpm install
python scripts/setup_sdk.py
python scripts/build_content.py
python scripts/generate_audio.py
pnpm build:web
python scripts/build_apk.py
python tests/test_app.py
python tests/test_assets.py
python tests/test_bridge.py
```

`build_content.py` dùng PDF tại các đường dẫn đã cung cấp trong cuộc thảo luận. Khi chuyển dự án sang máy khác, cập nhật các đường dẫn hoặc dùng `www/data.js` và `content/catalog.json` đã tạo sẵn nếu không đổi nội dung. Để build lại APK với nội dung hiện tại, chỉ cần `pnpm build:web` và `python scripts/build_apk.py`; MP3 đã có sẵn, không cần tạo lại.

Tạo âm thanh cần mạng ở máy build; app đã cài không cần mạng. Script bỏ qua file đã khớp văn bản/giọng và tạo lại các từ thay đổi.

## Phạm vi bản 1.0

Tiếng Anh ưu tiên bộ từ Glossary, chưa tách danh sách theo từng tiết Getting Started/Skills. Tiếng Hoa là bộ từ học được chọn từ các đề, không phải toàn bộ danh mục HSK 4 và không phải mô phỏng đầy đủ một kỳ thi. Chưa có luyện viết nét chữ, đồng bộ nhiều máy, tự thêm từ hoặc giọng đọc câu ví dụ. Các chức năng này có thể mở rộng trên nền dữ liệu hiện tại.

## Kiểm tra bản giao

- Build Java/Dex, đóng gói APK và kiểm tra chữ ký v2/v3: đạt.
- Các luồng học, ôn, trắc nghiệm, nhập từ, tìm kiếm, từ yêu thích, sáng/tối, lưu tiến độ, sao lưu và khôi phục: đạt trên Chromium, với kiểm tra chiều ngang màn hình 320–700 px.
- Giao tiếp JavaScript với các phương thức Android: đạt kiểm tra hợp đồng bằng bridge giả lập, bao gồm lần cài mới và dữ liệu trống.
- 414 MP3: đối chiếu hash và byte trong APK, lưu không nén để MediaPlayer mở trực tiếp, giải mã được và có tín hiệu âm thanh: đạt.
- Chưa chạy trên điện thoại Android thật. Máy ảo Android trên máy build bị lỗi khởi động ở QEMU, trước khi cài app; kiểm tra Android trực tiếp chưa thực hiện được. Phần inset Android 15 và trải nghiệm trên từng dòng điện thoại vẫn cần kiểm tra thiết bị.

Các báo cáo nằm trong `output/*-test-report.json`; ảnh giao diện được chụp từ kiểm tra Chromium, không phải ảnh điện thoại thật.
