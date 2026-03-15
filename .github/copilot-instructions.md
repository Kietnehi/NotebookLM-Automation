# Hướng dẫn Copilot cho NotebookLM Automation

## Tổng quan dự án

Đây là công cụ tự động hóa Python sử dụng Playwright để tương tác với Google NotebookLM. Công cụ tự động hóa:
- Tải tài liệu từ thư mục cục bộ
- Yêu cầu AI tạo tổng quan (video/audio)
- Tải xuống và sắp xếp các tệp đầu ra

**Công nghệ:** Python 3.8+, Playwright, Chrome persistent context

## Lệnh Build & Run

```bash
# Cài đặt dependencies
pip install playwright
playwright install

# Chạy automation
python main.py

# Script yêu cầu tương tác thủ công tại 2 điểm:
# 1. Sau khi upload tài liệu xong (nhấn Enter)
# 2. Sau khi tạo video/audio xong (nhấn Enter)
```

## Kiến trúc & Các file quan trọng

```
NotebookLM-Automation/
├── main.py              # Script automation chính với Playwright
├── Documentss/          # Input: PDFs và tài liệu cần upload
├── Video/               # Output: File video/audio đã tải xuống
├── Images_NoteBookLM/   # Output: File ảnh được tự động sắp xếp
├── images/              # Hình ảnh dự án (sơ đồ workflow)
└── README.md            # Tài liệu tiếng Việt
```

## Cấu hình

Tất cả đường dẫn được cấu hình trong `main.py` ở phần đầu file:

```python
FOLDER_PATH = r"path\to\Documentss"          # Thư mục tài liệu đầu vào
VIDEO_SAVE_PATH = r"path\to\Video"           # Thư mục lưu media
IMAGE_SAVE_PATH = r"path\to\Images_NoteBookLM" # Thư mục lưu ảnh
USER_DATA_DIR = r"path\to\ChromeAuto"       # Chrome profile để giữ phiên đăng nhập
```

**Quan trọng:** Script sử dụng Chrome persistent context (`USER_DATA_DIR`) để duy trì phiên đăng nhập Google. Trước lần chạy đầu tiên:
1. Tạo thư mục ChromeAuto
2. Đăng nhập thủ công qua Chrome với `--user-data-dir` hoặc chạy script lần đầu và đăng nhập tương tác
3. Đảm bảo tất cả cửa sổ Chrome dùng profile này đã đóng trước khi chạy

## UI Locators & Ngôn ngữ

Script sử dụng các selector dựa trên text tiếng Việt (ví dụ: "Tạo", "Tải tệp lên", "Tổng quan bằng video"). Nếu giao diện NotebookLM của bạn dùng tiếng Anh, bạn phải:
- Đổi ngôn ngữ Google sang tiếng Việt, HOẶC
- Cập nhật các text locator trong `main.py` cho khớp với ngôn ngữ UI của bạn

## Các lỗi thường gặp

1. **Lỗi "Profile in use"**: Đóng tất cả cửa sổ Chrome dùng cùng `USER_DATA_DIR` trước khi chạy
2. **Yêu cầu đăng nhập**: Lần chạy đầu tiên cần đăng nhập Google thủ công (bao gồm 2FA nếu bật)
3. **Cập nhật Chrome**: Sau khi Chrome cập nhật, chạy `playwright install chromium` để đồng bộ driver
4. **Dừng thủ công**: Script dừng 2 lần chờ nhấn Enter - không bỏ qua
5. **Selector failure**: Nếu text UI thay đổi, selectors sẽ fail; cập nhật chúng theo giao diện NotebookLM hiện tại

## Hướng dẫn Phát triển

- Script được thiết kế cho **interactive** use, không phải automation hoàn toàn headless
- Error handling dùng try/except để thoát khỏi lỗi và giữ workflow chạy tiếp
- File downloads được tổ chức theo extension (ảnh sắp xếp riêng)
- Filenames được trích xuất từ web UI để đảm bảo chính xác

## Kiểm tra Thay đổi

Khi sửa `main.py`:
1. Test với tài liệu nhỏ trước
2. Quan sát browser để verify selectors vẫn hoạt động
3. Kiểm tra file tải xuống về đúng thư mục
4. Verify script xử lý lỗi graceful mà không crash

## Ghi chú cho AI Agents

- Giữ thay đổi tối thiểu và tập trung vào issue cụ thể
- Bảo tồn cấu trúc và pattern error handling hiện tại
- Khi cập nhật selectors, tìm tất cả occurrences của pattern text tiếng Việt
- Không xóa các điểm dừng thủ công - chúng là cố ý cho processing time
- Dự án dùng relative paths; giữ pattern này khi thêm config options mới
