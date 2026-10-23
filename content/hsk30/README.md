# New HSK Course · HSK 3.0

| Bộ sách | Bài | Mục từ theo bài |
| --- | --- | ---: |
| Cấp 1 | 1–15 | 330 |
| Cấp 2 | 1–15 | 211 |
| Cấp 3 | 1–18 | 483 |
| Cấp 4 · Tập 1 | 1–10 | 392 |
| Cấp 4 · Tập 2 | 11–20 | 407 |
| Tổng | 68 | 1.823 |

Nguồn là năm PDF New HSK Course người dùng cung cấp. Tên file đầy đủ nằm trong `scripts/extract_hsk30.py` và trong từng bản ghi catalog. Không sửa hoặc đóng gói PDF gốc.

Từ vựng và số bài lấy từ bảng từ cuối từng quyển: PDF 137–142 (cấp 1), 156–161 (cấp 2), 186–193 (cấp 3), 130–136 (cấp 4 tập 1), 128–135 (cấp 4 tập 2). Dừng trước danh sách tên riêng. Giữ từ mở rộng (*) và giữ riêng mỗi lần một từ được bảng từ gắn với bài khác. Vì vậy số trên là số mục học theo bài, không phải số từ duy nhất hay toàn bộ danh mục của kỳ thi HSK.

Mục lục được đối chiếu trên PDF 12–14, 12–14, 10–12, 8–10 và 2–4 tương ứng năm quyển. Từ được nhóm theo số bài của sách; số thứ tự hiển thị trong bài là thứ tự mục học được tạo từ bảng từ, không trình bày là số thứ tự từ mới in trong phần bài khóa.

`words.json` và `source-audit.json` giữ chữ, số bài, trang nguồn, OCR/tọa độ ban đầu khi có và các hiệu chỉnh đã rà soát. Trang PDF 190 cấp 3 bị nghiêng khoảng 14,4 độ; tọa độ các hàng đã được hiệu chỉnh trước khi ghép từ với số bài. Bổ sung thủ công các mục OCR bỏ sót: 们 (cấp 1 bài 1, PDF 139), 一 (cấp 1 bài 4, PDF 142), 白色 (cấp 2 bài 4, PDF 156) và 笔记本（电脑） (cấp 3 bài 11, PDF 187). Mục cuối hiển thị 笔记本电脑 và chấp nhận 笔记本 khi luyện nhập.

Nghĩa tiếng Việt được biên soạn theo từ/ngữ cảnh; một số nghĩa và pinyin được tái sử dụng từ kho cũ rồi hiệu chỉnh theo bộ sách trong `overrides.json`. Các thành tố như 医, 感, 员, 性, 者 vẫn được giữ vì có trong bảng từ. Các chữ đa âm cần xác định cách đọc có cụm `speechText` và chú thích âm thanh trong app.

Có 84 mục dùng tiêu đề bài làm ví dụ, được ghi rõ **Trích tiêu đề bài**. Các mục còn lại có thông báo chưa có ví dụ; chưa trích toàn bộ câu từ bài khóa và không tạo câu giả làm câu sách. Mỗi mục có MP3 giọng tổng hợp ngoại tuyến; ví dụ bằng chữ chưa có audio riêng.

HSK 3.0 có nhóm, mã từ và tiến độ riêng. Giữ nguyên mọi bản ghi/MP3 của 1.8.0. Không chuyển tiến độ giữa các bộ chỉ vì từ có cùng chữ.

Build lại từ dữ liệu đã rà soát:

```powershell
python scripts/build_hsk30.py
python scripts/generate_audio.py
pnpm build:web
python scripts/build_apk.py
python tests/test_hsk30.py
```

OCR chỉ ghi cache vào `tmp/hsk30`, không ghi đè dữ liệu đã rà soát:

```powershell
python scripts/extract_hsk30.py 3 186-193 --source-dir "D:\LeNgocBE\Download\Telegram Desktop"
```
