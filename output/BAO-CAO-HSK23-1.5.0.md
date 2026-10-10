# Lingo 1.5.0 — Giáo trình HSK 2 và HSK 3

APK: `Lingo-SoTuVung-1.5.0.apk`, khoảng 32,05 MiB. Package `vn.lnb.sotuvung`, versionCode 6, Android 8.0 trở lên. Giữ cùng khóa ký để cài đè bản 1.0–1.4. Không gỡ bản cũ trước khi cập nhật; nên xuất sao lưu trong Cài đặt. SHA-256 nằm trong `SHA256.txt` và báo cáo phát hành JSON.

## Nội dung

- HSK 2: 169 mục từ của 15 bài, theo từ mới được đánh số, gồm các từ mở rộng.
- HSK 3: 314 mục từ của 20 bài. Tên riêng bên ngoài từ mới không được đưa vào danh sách.
- Mỗi từ có nghĩa tiếng Việt, pinyin, loại từ, trang PDF và giọng đọc ngoại tuyến. Âm đa nghĩa được xác định bằng cụm ngắn và chú thích; gồm 得, 着, 长, 还, 为, 教, 只, 地.
- Có 481 từ mới với ví dụ/trích đoạn từ tài liệu, trong đó ba câu hoàn thành bài tập điền từ có nhãn riêng. Nghĩa và bản dịch tiếng Việt được biên soạn theo ngữ cảnh.
- Giữ nguyên toàn bộ 2.422 mục từ cũ và MP3; tổng 2.905 từ, 130 nhóm bài học. Cài mới hoặc nâng cấp đều dùng cùng dữ liệu nội dung.

## Giới hạn nguồn HSK 3

PDF được cung cấp thiếu trang sách 168–169: ngay sau trang sách 167 là 170. Đây là hai trang bài 18 chứa phần từ mới/khóa văn. Vì vậy 17 từ của bài 18 được đối chiếu từ mục lục PDF trang 14 và bảng từ vựng tổng hợp ở cuối sách khi có. Số thứ tự trong app ở bài này là thứ tự mục lục, không được gắn nhãn là số từ mới đã xác minh trên hai trang bị thiếu. Nguồn và cảnh báo có trong phần giới thiệu bài và từng từ.

Các ví dụ bài 18 dùng những trang còn lại của chính giáo trình, bao gồm phần chú thích, bài tập, tiêu đề bài và một trích đoạn bài 19. Ba câu điền đáp án được phân biệt bằng nhãn **Câu bài tập đã điền đáp án**. Hai từ **万** và **嘴** chưa có ví dụ đã đối chiếu, app hiển thị lý do thay vì thêm ví dụ không có nguồn. Hai từ vẫn có nghĩa, pinyin, audio và hoạt động trong tất cả cách luyện. Có thể bổ sung sau khi có PDF đầy đủ với cùng mã từ.

## Học và tương thích

Thêm nút HSK 2/3 ở Bài học, Kho từ, Tiến độ và Từ hay sai. Ôn đến hạn, đáp án nhiễu, bài gần nhất và lịch sử sai tách theo cấp. Học thẻ, trắc nghiệm chọn nghĩa/nghe/chọn từ, nhập từ, luyện lại cuối lượt và Đã nắm vững dùng cơ chế hiện có. Sao lưu cũ vẫn nhập được; sao lưu mới giữ cả tiến độ cấp mới và lịch sử sai cũ.

## Kiểm tra

Kiểm tra chuyên biệt xác nhận mã/nội dung cũ giữ nguyên, từng bài có đúng số thứ tự, có trang nguồn, các trường cần thiết và nhãn giới hạn nguồn. Kiểm tra cài mới qua trạng thái trống, khôi phục 1.4, cách ly các cấp, đáp án, bài gần nhất, ôn đến hạn, luyện sai/luyện lại, nắm vững, nhập dạng ngắn, thẻ, nghe và cầu nối âm thanh. Kiểm tra lưu sau tải lại và vòng sao lưu, giao diện sáng/tối ở 320/360/390/700 px.

Kiểm tra hồi quy tiếng Anh, HSK 4.1/4.2, HSK 5.1/5.2, lịch sử sai và giao diện/cầu nối Android. APK được kiểm tra chữ ký, phiên bản, package, Android tối thiểu, zipalign, toàn bộ MP3 theo manifest và khả năng giải mã âm thanh. Báo cáo chi tiết trong các file `*-test-report.json`.

Chưa thử trên điện thoại Android thật. Kiểm tra giao diện và trạng thái dùng Chromium với cầu nối Android giả lập; kiểm tra chữ ký/tài nguyên thực hiện trên APK đã build.

## Build nội dung

`content/hsk23/words.txt`, `examples.tsv`, `provenance.json` và `source-audit.json` chứa bản biên tập và đối chiếu. `scripts/build_hsk23.py` dùng các file này để build lại mà không cần OCR. `scripts/extract_hsk23.py` là công cụ đọc lại nguồn scan, dùng cache trong `tmp/hsk23/` và các đường dẫn PDF đã cung cấp. Không đóng gói PDF vào APK; âm thanh đã nằm sẵn trong app.
