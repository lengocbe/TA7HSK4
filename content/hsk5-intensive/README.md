# HSK 5 · Luyện chuyên sâu

Đã nhận 24 PDF, thống kê trong books.json. Bản 1.12.0 bổ sung từ vựng của **HSK5词汇精讲精练.pdf**: 1.300 mục, 81 Unit (80 Unit × 16 từ, Unit 81 có 20 từ). Các sách khác chưa phát hành.

## Phạm vi bản 1.12.0

Từ lấy từ bảng đầu mỗi Unit, trang PDF 9 + 4 × (Unit − 1), không nhập đáp án/bài tập hoặc câu ví dụ. Có chữ giản thể, pinyin, nghĩa tiếng Việt và audio tổng hợp ngoại tuyến. Nghĩa dùng dữ liệu từ vựng đã có và điều chỉnh theo ngữ cảnh; các từ đa âm được rà riêng. Tiến độ theo mã từ riêng cho sách. Các bộ trước giữ nguyên bản ghi và audio.

reviewed.json lưu dữ liệu phát hành và chứng cứ dòng nguồn. OCR toàn trang được đối chiếu với OCR tách cột và số ô trong bảng; các ô mất hoặc dính chữ được sửa từ ảnh nguồn. Không dùng số từ trên bìa để tự thêm mục thiếu từ sách khác.

## Các sách đang xử lý

- 新HSK词汇突破5级 V2.pdf: OCR xong 132 trang từ vựng, đang đối chiếu mục từ, chưa xuất bản.
- HSK 5 Vocabulary Workbook.pdf: OCR xong bảng đáp án 320–348; đang kiểm tra số thứ tự và lỗi in trong nguồn, chưa xuất bản.
- 新HSK5000词分级词典  4-5级.pdf: đang trích danh mục 1.300 từ cấp 5, PDF 31–54. Không nhập lẫn 600 từ cấp 4.
- Conquering New HSK5 Vocabulary.pdf: đang OCR phần từ vựng theo chủ đề; chưa xuất bản.
- Các sách đọc/nghe/viết/ngữ pháp/đề thi vẫn trong danh sách nguồn chờ xử lý. Chưa có audio đề nghe gốc.

## Tái tạo

extract_hsk5_intensive.py tạo cache OCR từng trang; extract_hsk5_intensive_grid.py đọc riêng cột từ của sách 精讲精练. parse_hsk5_intensive*.py tạo bản nháp để đối chiếu. build_hsk5_intensive.py chỉ xuất reviewed.json đã duyệt, không lấy bản nháp. Sau đó chạy generate_audio.py, build:web, build_apk.py.

tests/test_hsk5_intensive.py kiểm tra chặn dữ liệu chưa duyệt và UI với fixture tách biệt; tests/test_hsk5_intensive_release.py kiểm tra dữ liệu thật, giữ nguyên 1.11.0 và học/ôn/sao lưu trên màn hình nhỏ. Chưa thử cài trên điện thoại thật.
