# Lingo 1.4.0 — Ôn từ trả lời sai

Bản cài: `Lingo-SoTuVung-1.4.0.apk`, khoảng 26,74 MiB. Package `vn.lnb.sotuvung`, versionCode 5, Android 8.0 trở lên. Chữ ký giống các bản 1.0–1.3 để cài đè; không gỡ app cũ trước khi nâng cấp. SHA-256: `c8c09d17f4c727a98bf8ebfdfcdc58857790f0d352c7b4f142c55ca78aaed34f`.

## Tính năng

- Cuối lượt hiện danh sách từ sai và Luyện lại câu sai. Lượt mới chỉ lấy từ vừa sai và giữ cách luyện; hỗ trợ chọn nghĩa, nhớ từ qua nghĩa, nghe và nhập từ.
- Từ hay sai trên Trang chủ/Kho từ: luyện tất cả theo bộ lọc, nhiều từ đã chọn hoặc từng từ. Có tìm kiếm và lọc Tiếng Anh, HSK 4 Luyện theo đề/4.1/4.2, HSK 5.1/5.2.
- Lưu số lần sai, thời điểm gần nhất và cách luyện theo mã từ. Chặn đáp án lặp và nút Tiếp cũ làm bỏ qua câu chưa trả lời.
- Trả lời đúng vẫn giữ lịch sử. Đã nắm vững đưa từ khỏi danh sách cần luyện, giữ lịch sử và cho khôi phục. Trả lời sai lần sau tự đưa lại vào cần luyện.
- Giữ nguyên toàn bộ 2.422 mục từ, bài học và giọng đọc của 1.3.0. Đánh giá Quên trên thẻ không được ghi thành lỗi trắc nghiệm.
- Sao lưu mới giữ lịch sử và trạng thái nắm vững. Sao lưu cũ vẫn nhập được, giữ tiến độ và khởi tạo lịch sử mới rỗng. Không tái dựng các câu sai trước 1.4.0.

## Kiểm tra

`tests/test_mistakes.py` kiểm tra cả bốn cách luyện, sai/đúng/luyện lại, bấm lặp, các bộ lọc, chọn từ, đánh dấu nắm vững, sai lại, lưu sau tải lại, vòng xuất/nhập sao lưu, bản sao lưu cũ và từ chối lịch sử không hợp lệ mà không thay dữ liệu đang có. Kiểm tra giao diện sáng/tối ở chiều rộng 320/360/390/700 px.

Các kiểm tra hồi quy `test_app.py`, `test_bridge.py`, `test_hsk4.py`, `test_hsk5.py`, `test_hsk52.py` đều đạt. Kiểm tra chữ ký, package, phiên bản, Android tối thiểu và căn chỉnh APK đạt; các bản 1.0–1.4 dùng cùng chứng chỉ. Báo cáo chi tiết nằm trong các file `*-test-report.json`.

Kiểm tra giao diện dùng Chromium và cầu nối Android giả lập; kiểm tra APK thực hiện trên file đã build. Chưa thử cài mới, cài đè hoặc sử dụng trên điện thoại Android thật.
