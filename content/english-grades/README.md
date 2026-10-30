# Global Success lớp 6, 8, 9 — 1.13.0

Nguồn là bốn PDF người dùng cung cấp trong X:/TA6789; cả ba lớp đều được xác nhận từ bìa và mục lục là Global Success. sources.json ghi tên file nguyên gốc, số trang, trang Glossary và SHA-256. Không đóng gói PDF vào APK.

| Lớp | Unit | Mục học |
|---|---:|---:|
| 6, gộp hai tập | 1–12 | 208 |
| 8 | 1–12 | 279 |
| 9 | 1–12 | 265 |

Tổng thêm 752 mục trong 36 Unit và 12 nhóm Review. Review dùng chung mã từ với ba Unit tương ứng. Từ lặp ở các Unit hoặc lớp khác nhau có mã riêng để theo dõi ngữ cảnh/tiến độ. Giữ nguyên 264 mục lớp 7 và toàn bộ dữ liệu của 1.12.0.

## Phạm vi và biên tập

Dùng bảng Glossary cuối sách, không coi đây là toàn bộ từ xuất hiện trong bài khóa. Ghép lại những cụm từ bị cắt dòng (railway station, natural wonder, floating market, electric cooker, washing machine...). Không nhập dòng phiên âm hoặc phần giải thích chữ viết tắt thành từ riêng. Các lỗi OCR như recydle, musde, stomm, camier pigeon được sửa theo chữ nguồn.

TSV từng lớp lưu chữ, IPA và nghĩa tiếng Việt đã biên tập. Phiên âm được chuẩn hóa thành ký tự IPA dễ đọc; nghĩa giữ theo ngữ cảnh bài, ví dụ compass lớp 6 Unit 1 là com-pa, Unit 5 là la bàn. Live nghĩa trực tiếp, permit và estimate dùng cụm ngắn trong audio để rõ cách đọc; thẻ có chú thích. Âm thanh tổng hợp Anh Anh, không phải audio gốc của sách. Các mục mới chưa có câu ví dụ và được thông báo trên thẻ.

source-audit.json giữ dòng OCR và trang PDF cho từng mã từ, kèm bản ghi đã biên tập. glossary-draft.json chỉ là kết quả nhận dạng phục vụ đối chiếu; builder dùng TSV đã biên tập, không tự công bố OCR.

## Tái tạo và xác minh

extract_english_grades.py tạo cache OCR từ các PDF nguồn; parse_english_grades.py tách hàng Glossary. build_english_grades.py chỉ thay dữ liệu grade 6/8/9, bảo toàn bản ghi lớp 7 và tiếng Hoa. Sau đó chạy generate_audio.py, build:web, build_apk.py.

Bộ lọc lớp áp dụng cho bài học, kho từ, tiến độ, từ hay sai, ôn đến hạn và đáp án trắc nghiệm. Sao lưu cũ vẫn nhập được; bài lớp 7 cũ dùng grade mặc định 7 và giữ mã từ cũ. Chưa thử trên điện thoại thật.
