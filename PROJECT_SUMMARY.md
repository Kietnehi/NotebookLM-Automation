# 📋 Tóm Tắt Dự Án NotebookLM Automation

## 🎯 Tổng Quan Dự Án

**NotebookLM Automation** là công cụ Python sử dụng Playwright để tự động hóa các tương tác với Google NotebookLM. Công cụ này tối ưu hóa quy trình tải lên tài liệu, yêu cầu AI tạo tổng quan (video/audio), và tự động tải xuống cũng như sắp xếp các file đầu ra.

**Mục đích:** Tiết kiệm thời gian và công sức khi làm việc với NotebookLM, đặc biệt hữu ích cho các nhà nghiên cứu, sinh viên và bất kỳ ai muốn tận dụng sức mạnh AI để phân tích tài liệu.

---

## ✨ Tính Năng Chính

- **🆕 Tạo Notebook tự động:** Khởi tạo không gian làm việc mới trên NotebookLM
- **📤 Tải lên tự động:** Quét và tải lên toàn bộ tài liệu từ thư mục đã cấu hình
- **🎬 Tạo Media tự động:** Tự động click để tạo "Tổng quan bằng video/audio"
- **⬇️ Tải xuống thông minh:** Quét toàn bộ bản ghi/tệp đính kèm được tạo, trích xuất tên file từ giao diện web để lưu trữ chính xác
- **📁 Sắp xếp tự động:** Tự động di chuyển file hình ảnh (`.jpg`, `.png`, `.webp`,...) sang thư mục riêng, giữ video/audio ở thư mục chính
- **🔐 Đăng nhập bền vững:** Sử dụng Chrome Profile cục bộ (User Data Dir) để tránh xác thực lại

---

## 🛠️ Công Nghệ Sử Dụng

| Thành Phần | Công Nghệ |
|------------|-----------|
| Ngôn ngữ | Python 3.8+ |
| Tự động hóa | Playwright |
| Trình duyệt | Chrome (persistent context) |
| Dịch vụ mục tiêu | Google NotebookLM |
| Quản lý file | Thư viện `os`, `shutil`, `re` |

---

## 📂 Cấu Trúc Dự Án

```
NotebookLM-Automation/
├── main.py                      # Script tự động hóa chính với Playwright
├── Documentss/                  # Input: PDFs và tài liệu cần tải lên
├── Video/                       # Output: File video/audio đã tải xuống
├── Images_NoteBookLM/           # Output: File hình ảnh đã tải xuống
├── images/                      # Hình ảnh dự án (sơ đồ workflow)
├── .github/
│   └── copilot-instructions.md # Hướng dẫn cho AI Agent
├── README.md                    # Tài liệu tiếng Việt
└── PROJECT_SUMMARY.md          # File này
```

---

## ⚙️ Cấu Hình

Tất cả đường dẫn được cấu hình trong `main.py` ở phần đầu file:

```python
FOLDER_PATH = r"C:\Users\ADMIN\Desktop\Github Fulll Project\NotebookLM-Automation\Documentss"
VIDEO_SAVE_PATH = r"C:\Users\ADMIN\Desktop\Github Fulll Project\NotebookLM-Automation\Video"
IMAGE_SAVE_PATH = r"C:\Users\ADMIN\Desktop\Github Fulll Project\NotebookLM-Automation\Images_NoteBookLM"
USER_DATA_DIR = r"C:\Users\ADMIN\Desktop\ChromeAuto"
```

**Quan trọng:** Script sử dụng Chrome persistent context (`USER_DATA_DIR`) để duy trì phiên đăng nhập Google.

---

## 🚀 Bắt Đầu Nhanh

### 1. Cài Đặt Dependencies

```bash
pip install playwright
playwright install
```

### 2. Thiết Lập Chrome Profile

1. Tạo thư mục cho Chrome profile (ví dụ: `C:\Users\ADMIN\Desktop\ChromeAuto`)
2. **Đóng tất cả cửa sổ Chrome** đang dùng profile đó
3. Chạy script một lần để kích hoạt đăng nhập thủ công, HOẶC mở Chrome thủ công với:
   ```bash
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\ADMIN\Desktop\ChromeAuto"
   ```
4. Đăng nhập tài khoản Google (với 2FA nếu bật) và cấp quyền NotebookLM
5. Đóng Chrome - session đã được lưu

### 3. Chuẩn Bị Input

Đặt tất cả tài liệu (PDFs, v.v.) vào thư mục `Documentss/`.

### 4. Chạy Tự Động Hóa

```bash
python main.py
```

**Lưu ý:** Script yêu cầu tương tác thủ công tại 2 điểm:
- Sau khi tải lên tài liệu xong (nhấn Enter)
- Sau khi tạo video/audio xong (nhấn Enter)

---

## 🔄 Cách Hoạt Động

1. **Khởi tạo:** Tạo thư mục output nếu chưa tồn tại
2. **Kiểm tra đăng nhập:** Xác minh giao diện NotebookLM có thể truy cập; nếu không, yêu cầu user đăng nhập thủ công
3. **Tải lên tài liệu:** Điều hướng đến NotebookLM, tải lên tất cả file từ `Documentss/`
4. **Chờ xử lý:** Tạm dừng để user xác nhận tải lên hoàn tất
5. **Tạo Media:** Click các nút để tạo tổng quan video/audio
6. **Chờ tạo:** Tạm dừng để user xác nhận tạo hoàn tất
7. **Tải xuống file:** Quét trang để tìm artifact có thể tải, trích xuất tên file, tải xuống vào `Video/`
8. **Tự sắp xếp:** Di chuyển file hình ảnh từ `Video/` sang `Images_NoteBookLM/`
9. **Dọn dẹp:** Đóng các tab thừa, giữ trạng thái trình duyệt sạch sẽ

---

## 🐛 Vấn Đề Thường Gặp & Giải Pháp

| Vấn đề | Nguyên nhân | Giải pháp |
|--------|-------------|-----------|
| **"Profile in use"** | Chrome đang dùng `USER_DATA_DIR` | Đóng tất cả cửa sổ Chrome dùng profile đó |
| **Yêu cầu đăng nhập** | Lần chạy đầu hoặc session hết hạn | Đăng nhập thủ công khi được hỏi (script chờ) |
| **Chrome update mismatch** | Chrome cập nhật nhưng Playwright driver cũ | Chạy `playwright install chromium` |
| **Bỏ qua dừng thủ công** | Script có điểm dừng cố ý | Nhấn Enter khi được hỏi; không bỏ qua |
| **Selector failure** | Text UI thay đổi (khác ngôn ngữ) | Cập nhật text locators trong `main.py` cho khớp với UI NotebookLM hiện tại |

---

## 🎯 UI Locators & Ngôn Ngữ

Script sử dụng các selector dựa trên text tiếng Việt (ví dụ: "Tạo", "Tải tệp lên", "Tổng quan bằng video"). Nếu giao diện NotebookLM của bạn dùng tiếng Anh, bạn phải:

- Đổi ngôn ngữ Google sang tiếng Việt, **HOẶC**
- Cập nhật tất cả text locator trong `main.py` cho khớp với ngôn ngữ UI của bạn

---

## 🧪 Kiểm Tra & Xác Thực

Khi sửa `main.py`:

1. **Test với tài liệu nhỏ trước** (1-2 file)
2. **Quan sát browser** để verify selectors vẫn hoạt động
3. **Kiểm tra vị trí tải xuống** - file phải về đúng thư mục
4. **Verify error handling** - script phải xử lý failures gracefully mà không crash
5. **Test cả 2 điểm dừng** - đảm bảo Enter prompts hoạt động

---

## 📝 Hướng Dẫn Phát Triển

- Script được thiết kế cho **interactive** use, không phải automation hoàn toàn headless
- Error handling dùng try/except để thoát khỏi lỗi và giữ workflow chạy tiếp
- Downloads được tổ chức theo extension (ảnh sắp xếp riêng)
- Filenames được trích xuất từ web UI để đảm bảo chính xác
- **Không bao giờ xóa các điểm dừng thủ công** - chúng là cố ý cho processing time

---

## 🤝 Cho AI Agents (Copilot)

Khi làm việc trên dự án này:

- ✅ Giữ thay đổi tối thiểu và tập trung vào issue cụ thể
- ✅ Bảo tồn error handling patterns hiện tại
- ✅ Khi cập nhật selectors, tìm TẤT CẢ occurrences của pattern text tiếng Việt
- ✅ KHÔNG xóa các điểm dừng thủ công - chúng là bắt buộc
- ✅ Dự án dùng relative paths; giữ pattern này khi thêm config options mới
- ✅ Đọc `copilot-instructions.md` để xem hướng dẫn chi tiết

---

## 📊 Sơ Đồ Luồng Script

```mermaid
graph TD
    A[Bắt đầu main.py] --> B[Khởi tạo thư mục]
    B --> C[Khởi động Chrome với persistent context]
    C --> D{NotebookLM sẵn sàng?}
    D -->|Có| E[Tải lên tất cả tài liệu]
    D -->|Không| F[Yêu cầu đăng nhập thủ công]
    F --> G[User đăng nhập]
    G --> D
    E --> H[Chờ Enter (tải lên hoàn tất)]
    H --> I[Click nút tạo video/audio]
    I --> J[Chờ Enter (tạo hoàn tất)]
    J --> K[Quét và tải xuống artifacts]
    K --> L[Tự sắp xếp ảnh sang thư mục riêng]
    L --> M[Đóng tab thừa]
    M --> N[Hoàn tất]
```

---

## 🔐 Bảo Mật & Best Practices

- **Chrome Profile:** Giữ `USER_DATA_DIR` private; nó chứa login cookies
- **Input Validation:** Script giả định `Documentss/` chứa file hợp lệ
- **Error Recovery:** Graceful degradation - script tiếp tục sau non-critical errors
- **Manual Oversight:** Interactive pauses cho phép user can thiệp nếu cần

---

## 📚 Tài Nguyên Bổ Sung

- **Tài liệu đầy đủ:** Xem `README.md` (tiếng Việt)
- **Hướng dẫn Agent:** Xem `.github/copilot-instructions.md`
- **Mã nguồn:** `main.py` (logic tự động hóa chính)

---

## 📄 Giấy Phép

*(Xem file giấy phép repository để biết chi tiết)*

---

**Cập nhật lần cuối:** 15 tháng 3, 2026  
**Phiên bản:** 1.0  
**Trạng thái:** Đang phát triển
