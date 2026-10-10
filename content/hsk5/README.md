# Dữ liệu HSK 5.1

Nguồn: PDF Giáo trình chuẩn HSK5.1_c9f3aee3070d412769f85e5c79f1c5f9.pdf do người dùng cung cấp (159 trang quét). PDF không được đóng gói hoặc đưa vào Git.

- `words.txt`: các dòng `từ|loại từ|nghĩa`; đầu bài là `# số_bài`. Thứ tự dòng khớp số thứ tự từ mới trong sách. Có 723 mục / 18 bài, gồm từ đánh dấu (*), không gồm bảng tên riêng hoặc thuật ngữ riêng bên dưới bài.
- `examples.tsv`: `bài|số_từ_cách_nhau_bằng_dấu_phẩy|trang_PDF|câu_trích|bản_dịch`. Một câu có thể dùng cho nhiều từ. Dấu câu/ba chấm được chuẩn hóa; từ tách như 吵过架 được giữ nguyên theo câu nguồn. Bản dịch tiếng Việt phục vụ học từ.
- `provenance.json`: trang PDF, dấu mở rộng và nhãn OCR gốc của từng mục. Nhãn OCR chỉ dùng đối chiếu; văn bản sửa lỗi nằm trong `words.txt`. Đã sửa các lỗi nhận dạng 喉 → 唉, 毕竞 → 毕竟 và Z → 乙.
- `scripts/build_hsk5.py`: ghép dữ liệu; kiểm tra số lượng từng bài, ví dụ không bị gán trùng; đặt pinyin theo ngữ cảnh và cách viết rút gọn được chấp nhận.

Trang in trong phần bài học bằng số trang PDF + 10. Nguồn trên từng thẻ ghi riêng trang từ mới và trang câu trích. Một số câu đi qua hai trang.

Các mục 细节 (bài 1), 由来 (bài 6), 成语/则 (bài 7), 闹钟/危害 (bài 11) dùng tiêu đề gốc, được hiển thị nhãn Trích tiêu đề bài. 投篮 (bài 13) chưa tìm được câu phù hợp trong phần bài đọc và các trang bài tập đã rà; thẻ hiển thị trạng thái cần đối chiếu, không đưa từ đơn lẻ ra làm câu.

Giọng đọc chỉ cho từ, không cho câu ví dụ. Các chữ đa âm đơn lẻ được đặt `speechText` bằng chữ đồng âm khi cần buộc TTS đọc đúng thanh (ví dụ 背 đọc bēi), và ghi cả văn bản từ lẫn văn bản đọc trong manifest. Toàn bộ MP3 dùng ngoại tuyến. Kiểm tra tự động giải mã/độ dài/tín hiệu không thay cho việc nghe rà toàn bộ từng bản ghi.

Để cập nhật nội dung hiện có mà không cần các PDF HSK 4 cũ, chạy `python scripts/build_hsk5.py`. Script này giữ nguyên mọi trường dữ liệu cũ, chỉ thêm nhãn cấp 4; ghi lại riêng các bản ghi HSK 5.1.
