

# NotebookLM Automation Tool 🚀

<p align="center">
  <img src="https://www.gstatic.com/images/branding/product/2x/googleg_48dp.png" width="70"/>
</p>

<p align="center">
  <img src="images/workflow.png" width="850"/>
</p>

<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="50"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/playwright/playwright-original.svg" height="50"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" height="50"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" height="50"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" height="50"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" height="50"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Playwright-Automation-45ba4b?style=for-the-badge&logo=playwright&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google-NotebookLM-FBBC05?style=for-the-badge&logo=google&logoColor=black"/>
  <img src="https://img.shields.io/badge/AI-Powered-8A2BE2?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/Kietnehi/NotebookLM-Automation?style=social"/>
  <img src="https://img.shields.io/github/forks/Kietnehi/NotebookLM-Automation?style=social"/>
  <img src="https://img.shields.io/github/license/Kietnehi/NotebookLM-Automation?style=social"/>
</p>

---

Dự án này là một tập lệnh Python sử dụng Playwright để tự động hóa các thao tác trên **Google NotebookLM**. Tool giúp bạn tự động tải tài liệu lên, yêu cầu AI tạo tổng quan (Video/Audio), tự động tải xuống tất cả các tệp kết quả và phân loại chúng một cách gọn gàng. Đây là một giải pháp hoàn chỉnh giúp bạn tiết kiệm thời gian và công sức khi làm việc với NotebookLM, đặc biệt hữu ích cho các nhà nghiên cứu, sinh viên hoặc bất kỳ ai muốn tận dụng sức mạnh của AI để phân tích tài liệu.

---

## ✨ Tính năng chính

- **Tự động tạo Notebook mới:** Khởi tạo không gian làm việc mới trên NotebookLM.
- **Tự động Upload:** Quét và tải lên toàn bộ tài liệu từ thư mục cấu hình sẵn.
- **Tự động thao tác tạo Media:** Tự động click yêu cầu tạo "Tổng quan bằng video/audio".
- **Tải xuống thông minh:** Quét toàn bộ các bản ghi/tệp đính kèm được tạo ra, trích xuất tên file từ giao diện web để lưu trữ chuẩn xác.
- **Phân loại File tự động (Auto-sorting):** Tự động tách các file hình ảnh (`.jpg`, `.png`, `.webp`,...) sang thư mục riêng, giữ lại video/audio ở thư mục gốc.
- **Bảo lưu phiên đăng nhập:** Sử dụng Chrome Profile cục bộ (User Data Dir) nên không cần đăng nhập lại Google mỗi lần chạy.

## 🛠️ Yêu cầu hệ thống (Prerequisites)

1. Cài đặt [Python 3.8+](https://www.python.org/downloads/).
2. Cài đặt thư viện Playwright:
   ```bash
   pip install playwright
   playwright install
   ```
3. Đã đăng nhập sẵn Google trên một Chrome Profile cục bộ (để cấp quyền cho NotebookLM).


# 🤖 Hướng dẫn Thiết lập ChromeAuto cho NotebookLM Automation

Hướng dẫn này giúp bạn cấu hình trình duyệt Chrome để script có thể sử dụng lại **tài khoản Google đã đăng nhập sẵn**, giúp vượt qua các bước xác thực (2FA) và bảo mật khi chạy Playwright.

---

## 🛠 Bước 1: Tìm đường dẫn thực thi của Chrome
Để script khởi động đúng trình duyệt bạn đang dùng, hãy xác định file `chrome.exe`:
1. Mở Chrome.
2. Nhập `chrome://version/` vào thanh địa chỉ rồi nhấn Enter.
3. Tìm dòng **Executable Path** (Đường dẫn thực thi). 
   * *Thông thường là:* `C:\Program Files\Google\Chrome\Application\chrome.exe`

---

## 📂 Bước 2: Tạo thư mục dữ liệu người dùng (ChromeAuto)
Script của bạn sử dụng `USER_DATA_DIR` để lưu Session (phiên đăng nhập).
1. Tạo một thư mục mới tại đường dẫn: `C:\Users\ADMIN\Desktop\ChromeAuto` (hoặc bất kỳ đâu bạn muốn).
2. **Lưu ý quan trọng:** Đảm bảo tất cả các cửa sổ Chrome bình thường **phải được đóng lại** trước khi chạy script lần đầu để Playwright có thể khởi tạo dữ liệu vào thư mục này.

---

## 🔑 Bước 3: Đăng nhập tài khoản của bạn
Để script "nhớ" tài khoản, bạn thực hiện như sau:

1. **Chạy script lần đầu tiên:** Ở chế độ `headless=False` (như trong code của bạn).
2. **Đăng nhập thủ công:** Khi trình duyệt tự động mở lên trang NotebookLM, hãy thực hiện đăng nhập tài khoản Google của bạn (nhập Email, Mật khẩu, xác nhận 2FA nếu có).
3. **Kiểm tra:** Sau khi đăng nhập thành công vào giao diện NotebookLM, hãy tắt script.
4. **Kết quả:** Từ lần chạy thứ 2 trở đi, Playwright sẽ mở đúng thư mục `ChromeAuto` đó và bạn sẽ **luôn luôn ở trạng thái đã đăng nhập**.

---

## 📝 Cấu hình lại Code của bạn
Hãy đảm bảo các đường dẫn trong file Python khớp với máy tính của bạn:

```python
# --- THAY ĐỔI THEO MÁY CỦA BẠN ---
FOLDER_PATH = r"C:\Users\ADMIN\Desktop\Github Fulll Project\NotebookLM-Automation\Documentss"
VIDEO_SAVE_PATH = r"C:\Users\ADMIN\Desktop\Github Fulll Project\NotebookLM-Automation\Video"
IMAGE_SAVE_PATH = r"C:\Users\ADMIN\Desktop\Github Fulll Project\NotebookLM-Automation\Images_NoteBookLM"
USER_DATA_DIR = r"C:\Users\ADMIN\Desktop\ChromeAuto" # Nơi lưu session đăng nhập

```

---

## ⚠️ Lưu ý về bảo mật và lỗi

* **Không chia sẻ thư mục ChromeAuto:** Thư mục này chứa "Cookie" và "Token" đăng nhập của bạn. Nếu người khác có thư mục này, họ có thể vào tài khoản Google của bạn.
* **Lỗi "Profile in use":** Nếu bạn đang mở Chrome thủ công và chạy script cùng lúc với cùng một thư mục `USER_DATA_DIR`, script sẽ báo lỗi. Hãy đóng Chrome trước khi chạy automation.
* **Cập nhật Chrome:** Nếu Chrome cập nhật phiên bản mới, đôi khi bạn cần chạy lệnh `playwright install chromium` để đồng bộ lại driver.

---

## ⚙️ Cấu hình (Configuration)

Mở file script bằng trình soạn thảo và sửa lại các đường dẫn (Paths) sao cho phù hợp với máy tính của bạn ở phần **CẤU HÌNH ĐƯỜNG DẪN**:

- `FOLDER_PATH`: Thư mục chứa các tài liệu/file bạn muốn up lên NotebookLM.
- `VIDEO_SAVE_PATH`: Thư mục lưu các file Video/Audio (Tập lệnh sẽ tải mọi thứ về đây trước).
- `IMAGE_SAVE_PATH`: Thư mục lưu riêng các tệp hình ảnh.
- `USER_DATA_DIR`: Đường dẫn đến thư mục Profile Chrome của bạn (Dùng để giữ trạng thái đăng nhập Google). *Lưu ý: Bạn phải tắt toàn bộ các cửa sổ Chrome đang mở bằng Profile này trước khi chạy script.*
## Cấu trúc thư mục : 

```text
NotebookLM-Automation/
├── 📁 Documentss
│   └── 📄 2510.12323v1.pdf
├── 📁 Images_NoteBookLM
├── 📄 README.md
├── 📁 Video
└── 📄 main.py
```

## 🚀 Hướng dẫn sử dụng

1. Đảm bảo bạn đã đặt các tài liệu cần phân tích vào thư mục `FOLDER_PATH`.
2. Mở Terminal / Command Prompt và chạy script:
   ```bash
   python main.py
   ```
   *(Thay `main.py` bằng tên file code của bạn)*
3. **Quá trình chạy & Tương tác thủ công (QUAN TRỌNG):**
   - Tool sẽ mở Chrome và tự động tải tài liệu lên NotebookLM.
   - **TẠM DỪNG 1:** Terminal sẽ hiện thông báo yêu cầu bạn chờ NotebookLM xử lý xong tài liệu (chờ icon hết xoay vòng). Khi web đã load xong tài liệu, hãy quay lại Terminal và **NHẤN [ENTER]** để tiếp tục.
   - Tool sẽ tự động bấm nút "Tạo Tổng quan bằng video".
   - **TẠM DỪNG 2:** Chờ quá trình Render của Google hoàn tất. Khi video hiện nút Play trên web, quay lại Terminal và **NHẤN [ENTER]** để tool bắt đầu cào và tải toàn bộ file xuống.
4. Tool sẽ tự động tải file, đổi tên dựa trên UI, phân loại hình ảnh/video vào đúng thư mục và thông báo hoàn thành.
5. Nhấn `[ENTER]` lần cuối để đóng trình duyệt.

## ⚠️ Lưu ý

- **Ngôn ngữ Web:** Script hiện đang dò tìm các nút bấm bằng tiếng Việt trên giao diện Google NotebookLM (ví dụ: `Tạo`, `Tải tệp lên`, `Tổng quan bằng video`). Nếu giao diện Google của bạn đang ở tiếng Anh, vui lòng đổi ngôn ngữ Google sang tiếng Việt hoặc sửa lại các text locator trong code.
- Tool sẽ bỏ qua (escape) nếu gặp lỗi trong quá trình bóc tách từng tệp để đảm bảo luồng chạy không bị sập hoàn toàn.
## 🔗 Author's GitHub

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=120&section=header"/>

<p align="center">
  <a href="https://github.com/Kietnehi">
    <img src="https://github.com/Kietnehi.png" width="140" height="140" style="border-radius: 50%; border: 4px solid #A371F7;" alt="Avatar Truong Phu Kiet"/>
  </a>
</p>

<h3>🚀 Truong Phu Kiet</h3>

<a href="https://github.com/Kietnehi/NotebookLM-Automation">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=236AD3&background=00000000&center=true&vCenter=true&width=435&lines=NotebookLM+Automation+Tool;Google+NotebookLM+Workflow+Automation;Built+with+Python+%26+Playwright" alt="Typing SVG" />
</a>

<br/><br/>

<p align="center">
  <img src="https://img.shields.io/badge/SGU-Sai_Gon_University-0056D2?style=flat-square&logo=google-scholar&logoColor=white" alt="SGU"/>
  <img src="https://img.shields.io/badge/Base-Ho_Chi_Minh_City-FF4B4B?style=flat-square&logo=google-maps&logoColor=white" alt="HCMC"/>
</p>

<h3>🛠 Tech Stack</h3>
<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=docker,python,react,nodejs,mongodb,git,fastapi,pytorch&theme=light" alt="My Skills"/>
  </a>
</p>

<br/>

<h3>🌟 NotebookLM Automation Project </h3>
<p align="center">
  <a href="https://github.com/Kietnehi/NotebookLM-Automation">
    <img src="https://img.shields.io/github/stars/Kietnehi/NotebookLM-Automation?style=for-the-badge&color=yellow" alt="Stars"/>
    <img src="https://img.shields.io/github/forks/Kietnehi/NotebookLM-Automation?style=for-the-badge&color=orange" alt="Forks"/>
    <img src="https://img.shields.io/github/issues/Kietnehi/NotebookLM-Automation?style=for-the-badge&color=red" alt="Issues"/>
  </a>
</p>

<!-- Dynamic quote -->
<p align="center">
  <img src="https://quotes-github-readme.vercel.app/api?type=horizontal&theme=dark" alt="Daily Quote"/>
</p>

<p align="center">
  <i>Thank you for visiting! Don’t forget to click <b>⭐️ Star</b> to support the project.</i>
</p>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=80&section=footer"/>

</div>