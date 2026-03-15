import os
import shutil
import re
from playwright.sync_api import sync_playwright

# --- CẤU HÌNH ĐƯỜNG DẪN ---
FOLDER_PATH = r"C:\Users\ADMIN\Desktop\Github Fulll Project\NotebookLM-Automation\Documentss"
VIDEO_SAVE_PATH = r"C:\Users\ADMIN\Desktop\Github Fulll Project\NotebookLM-Automation\Video"
IMAGE_SAVE_PATH = r"C:\Users\ADMIN\Desktop\Github Fulll Project\NotebookLM-Automation\Images_NoteBookLM"
USER_DATA_DIR = r"C:\Users\ADMIN\Desktop\ChromeAuto

# Khởi tạo thư mục nếu chưa có
for path in [VIDEO_SAVE_PATH, IMAGE_SAVE_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"📁 Đã chuẩn bị thư mục: {path}")

def is_notebook_ready(page):
    create_button = page.locator("button:has-text('Tạo'), [role='button']:has-text('Tạo')").first
    upload_button = page.locator("button:has-text('Tải tệp lên'), [role='button']:has-text('Tải tệp lên')").first

    return create_button.is_visible() or upload_button.is_visible()

def wait_for_notebook_ready(page, timeout_ms=15000):
    elapsed_ms = 0
    interval_ms = 1000

    while elapsed_ms < timeout_ms:
        if is_notebook_ready(page):
            return True
        page.wait_for_timeout(interval_ms)
        elapsed_ms += interval_ms

    return False

def ensure_logged_in(page):
    if wait_for_notebook_ready(page, timeout_ms=10000):
        return

    print("\n" + "="*70)
    print("🔐 Có vẻ bạn chưa đăng nhập Google trong profile ChromeAuto.")
    print("1. Chrome sẽ được giữ nguyên để bạn đăng nhập thủ công.")
    print("2. Sau khi vào được giao diện NotebookLM, quay lại Terminal.")
    print("3. Nhấn [ENTER] để script kiểm tra lại và tiếp tục chạy.")
    print("="*70)

    input("\n👉 ĐĂNG NHẬP XONG RỒI NHẤN [ENTER] ĐỂ TIẾP TỤC...")

    page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")

    if not wait_for_notebook_ready(page, timeout_ms=30000):
        raise RuntimeError(
            "Không tìm thấy giao diện NotebookLM sau khi đăng nhập. "
            "Hãy kiểm tra xem bạn đã vào đúng trang và tài khoản có quyền truy cập NotebookLM chưa."
        )

def organize_downloaded_files():
    print("\n" + "="*50)
    print("🧹 ĐANG PHÂN LOẠI FILE (VIDEO VS HÌNH ẢNH)...")
    print("="*50)
    
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.svg')
    
    try:
        files_in_video_folder = os.listdir(VIDEO_SAVE_PATH)
        moved_count = 0

        for filename in files_in_video_folder:
            if filename.lower().endswith(image_extensions):
                source = os.path.join(VIDEO_SAVE_PATH, filename)
                destination = os.path.join(IMAGE_SAVE_PATH, filename)
                
                shutil.move(source, destination)
                print(f"📸 [IMAGE] -> {filename}")
                moved_count += 1
        
        if moved_count > 0:
            print(f"\n✅ Hoàn tất! Đã di chuyển {moved_count} ảnh vào: {IMAGE_SAVE_PATH}")
        else:
            print("ℹ️ Không tìm thấy tệp hình ảnh nào để chuyển.")
    except Exception as e:
        print(f"❌ Lỗi khi phân loại file: {e}")

def close_stray_tabs(context, main_page):
    # Một số click có thể mở tab phụ ngoài ý muốn; đóng tab đó để giữ đúng luồng.
    for p in list(context.pages):
        if p != main_page:
            try:
                p.close()
            except Exception:
                pass

def click_scoped_create_button(page, artifact_label):
    """
    Chỉ bấm nút "Tạo" nếu nó nằm trong đúng vùng chứa artifact cần tạo.
    Trả về True nếu click thành công, False nếu không tìm thấy nút đủ tin cậy.
    """
    artifact_key = artifact_label.strip().lower()

    # Ưu tiên nút trong dialog có chứa tên artifact.
    dialogs = page.locator("[role='dialog'], [aria-modal='true']")
    for i in range(dialogs.count()):
        dialog = dialogs.nth(i)
        try:
            if not dialog.is_visible():
                continue
            dialog_text = dialog.inner_text().lower()
            if artifact_key not in dialog_text:
                continue

            create_btn = dialog.get_by_role("button", name=re.compile(r"^\s*Tạo\s*$", re.IGNORECASE)).first
            if create_btn.is_visible():
                create_btn.click(force=True)
                return True
        except Exception:
            continue

    # Fallback: nút "Tạo" trong card/khối có chính text artifact.
    scoped_btn = page.locator(
        f"[aria-label*='{artifact_label}'] button:has-text('Tạo'), "
        f"[aria-label*='{artifact_label}'] [role='button']:has-text('Tạo')"
    ).first
    try:
        if scoped_btn.is_visible():
            scoped_btn.click(force=True)
            return True
    except Exception:
        pass

    return False

def activate_artifact_creation(page, context, artifact_label, selectors):
    """
    Kích hoạt tạo artifact theo selector cụ thể.
    Trả về dict trạng thái để log rõ: đã bấm card hay chưa, và đã bấm nút Tạo hay chưa.
    """
    trigger = None
    for selector in selectors:
        candidate = page.locator(selector).last
        try:
            candidate.wait_for(state="visible", timeout=4000)
            trigger = candidate
            break
        except Exception:
            continue

    if trigger is None:
        raise RuntimeError(f"Không tìm thấy vùng '{artifact_label}'.")

    trigger.scroll_into_view_if_needed()
    trigger.click(force=True)
    close_stray_tabs(context, page)
    page.wait_for_timeout(800)

    create_clicked = click_scoped_create_button(page, artifact_label)
    return {
        "trigger_clicked": True,
        "create_clicked": create_clicked,
    }

def run_automation():
    with sync_playwright() as p:
        context = None
        try:
            print(f"🌐 Đang khởi động Chrome...")
            
            context = p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=False,
                channel="chrome", 
                args=[
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled"
                ]
            )
            
            page = context.pages[0] if context.pages else context.new_page()
            
            print("🔗 Đang truy cập NotebookLM...")
            page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
            ensure_logged_in(page)

            # --- BƯỚC 1: TẠO NOTEBOOK MỚI ---
            print("🔍 Đang tìm nút tạo Notebook...")
            new_btn = page.locator("button:has-text('Tạo'), [role='button']:has-text('Tạo')").first
            new_btn.wait_for(state="visible", timeout=30000)
            new_btn.click()
            print("✅ Đã tạo Notebook mới.")

            # --- BƯỚC 2: UPLOAD FILES ---
            if os.path.exists(FOLDER_PATH):
                files = [os.path.join(FOLDER_PATH, f) for f in os.listdir(FOLDER_PATH) 
                         if os.path.isfile(os.path.join(FOLDER_PATH, f))]
                
                if files:
                    print(f"📂 Tìm thấy {len(files)} tệp. Đang chuẩn bị upload...")
                    page.wait_for_timeout(2000) 
                    
                    upload_target = page.locator("button:has-text('Tải tệp lên'), [role='button']:has-text('Tải tệp lên')").first
                    upload_target.wait_for(state="visible", timeout=15000)

                    with page.expect_file_chooser() as fc_info:
                        upload_target.click()
                    
                    file_chooser = fc_info.value
                    file_chooser.set_files(files)
                    
                    print("\n" + "!"*60)
                    print("🚀 ĐANG UPLOAD TÀI LIỆU...")
                    print("Vui lòng đợi NotebookLM xử lý xong các tài liệu (hết xoay vòng).")
                    input("👉 SAU ĐÓ NHẤN [ENTER] TẠI ĐÂY ĐỂ TIẾP TỤC TẠO VIDEO & BẢN ĐỒ HOẠ...")
                    print("!"*60 + "\n")
                    
                else:
                    print("⚠️ Thư mục Documentss đang trống!")
            else:
                print(f"❌ Không tìm thấy đường dẫn: {FOLDER_PATH}")

            # --- BƯỚC 3: KÍCH HOẠT TẠO VIDEO VÀ BẢN ĐỒ HOẠ ---
            
            # 3.1 Tạo Video Overview
            try:
                print("🎬 Đang yêu cầu tạo 'Tổng quan bằng video'...")
                video_status = activate_artifact_creation(
                    page,
                    context,
                    "Tổng quan bằng video",
                    [
                        "[aria-label*='Tổng quan bằng video']",
                        "div[role='button']:has-text('Tổng quan bằng video')",
                        "button:has-text('Tổng quan bằng video')",
                    ],
                )

                if video_status["create_clicked"]:
                    print("✅ Đã bấm card và nút 'Tạo' cho Video.")
                else:
                    print("✅ Đã bấm card Video. ")
            except Exception as e:
                print(f"⚠️ Không thể tự động bấm 'Tạo Video': {e}")

            page.wait_for_timeout(3000) # Nghỉ để UI cập nhật

            # 3.2 Tạo Bản đồ hoạ thông tin
            try:
                print("📊 Đang yêu cầu tạo 'Bản đồ hoạ thông tin'...")
                infographic_status = activate_artifact_creation(
                    page,
                    context,
                    "Bản đồ hoạ thông tin",
                    [
                        "div[aria-label='Bản đồ hoạ thông tin']",
                        "[role='button']:has-text('Bản đồ hoạ thông tin')",
                        "button:has-text('Bản đồ hoạ thông tin')",
                    ],
                )

                if infographic_status["create_clicked"]:
                    print("✅ Đã bấm card và nút 'Tạo' cho Bản đồ hoạ thông tin.")
                else:
                    print("✅ Đã bấm card Bản đồ hoạ thông tin. Không có nút 'Tạo' riêng — hệ thống tự động tạo.")
            except Exception as e:
                print(f"⚠️ Không thể tự động bấm 'Bản đồ hoạ': {e}")
                print("ℹ️ Đừng lo, bạn có thể tự bấm nút này trên trình duyệt bây giờ.")

            # --- BƯỚC 4: TẠM DỪNG ĐỢI NGƯỜI DÙNG XÁC NHẬN ---
            print("\n" + "="*70)
            print("⏳ HỆ THỐNG ĐANG DỪNG LẠI ĐỂ ĐỢI RENDER.")
            print("1. Hãy kiểm tra trình duyệt: Đảm bảo Video và Bản đồ hoạ ĐANG ĐƯỢC TẠO.")
            print("2. Nếu bước trước bị lỗi (⚠️), hãy tự tay bấm nút Tạo trên Chrome.")
            print("3. Đợi cho đến khi hết vòng xoay tải (Render xong).")
            print("="*70)
            
            input("\n👉 NHẤN [ENTER] TẠI ĐÂY ĐỂ BẮT ĐẦU QUY TRÌNH TẢI XUỐNG TẤT CẢ...")

            # --- BƯỚC 5: VÒNG LẶP TẢI XUỐNG ---
            menu_dots = page.locator(".studio-card button[aria-haspopup='menu'], .studio-card button[aria-label*='Xem thêm']")
            if menu_dots.count() == 0:
                menu_dots = page.locator("button[aria-haspopup='menu'], button[aria-label*='Xem thêm']")

            total_items = menu_dots.count()
            print(f"📦 Phát hiện {total_items} mục có thể tải xuống.")

            for i in range(total_items):
                try:
                    current_dot = menu_dots.nth(i)
                    current_dot.scroll_into_view_if_needed()

                    # --- LẤY TÊN HIỂN THỊ TỪ GIAO DIỆN CHUẨN XÁC NHẤT ---
                    file_title = f"NoteLM_BanGhi_{i+1}" # Tên dự phòng nếu lỗi
                    try:
                        # Đi ngược lên các thẻ cha để tìm container chung, sau đó lấy đúng thẻ có class 'artifact-title'
                        raw_text = current_dot.evaluate("""
                            (el) => {
                                let current = el;
                                // Đi ngược lên tối đa 5 cấp để tìm hàng chứa phần tử
                                for(let j=0; j<5; j++) {
                                    if(current.parentElement) {
                                        current = current.parentElement;
                                        // Tìm chính xác thẻ span chứa tiêu đề
                                        let titleNode = current.querySelector('.artifact-title');
                                        if(titleNode) {
                                            return titleNode.innerText.trim();
                                        }
                                    }
                                }
                                return null;
                            }
                        """)
                        if raw_text:
                            # Xóa các ký tự cấm của Windows (\, /, :, *, ?, ", <, >, |)
                            clean_title = re.sub(r'[\\/*?:"<>|]', "", raw_text).strip()
                            # Giới hạn độ dài tên file tránh lỗi đường dẫn quá dài
                            file_title = clean_title[:80] if len(clean_title) > 80 else clean_title
                    except Exception as e:
                        print(f"   ⚠️ Không bóc tách được tên UI, dùng tên mặc định.")

                    print(f"📥 Đang xử lý mục {i+1}/{total_items} [{file_title}]...")
                    
                    current_dot.click(delay=200)
                    page.wait_for_timeout(1500)
                    
                    download_btn = page.locator("div[role='menuitem']:has-text('Tải xuống'), span:has-text('Tải xuống'), button:has-text('Tải xuống')").last
                    
                    if download_btn.is_visible():
                        with page.expect_download() as download_info:
                            download_btn.click(delay=200)
                        
                        download = download_info.value
                        
                        # Tách lấy phần đuôi mở rộng của file gốc (VD: .wav, .mp4, .txt)
                        original_filename = download.suggested_filename
                        _, file_extension = os.path.splitext(original_filename)
                        
                        # Gắn số thứ tự ở đầu phòng trường hợp có nhiều file trùng tên trên UI
                        save_name = f"{i+1} - {file_title}{file_extension}"
                        save_path = os.path.join(VIDEO_SAVE_PATH, save_name)
                        
                        download.save_as(save_path)
                        print(f"   ✅ Đã tải: {save_name}")
                        
                        page.wait_for_timeout(2000)
                    else:
                        print(f"   ⚠️ Không thấy nút 'Tải xuống' cho mục này.")
                    
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(1000)

                except Exception as inner_e:
                    print(f"   ❌ Lỗi tại mục {i+1}: {inner_e}")
                    page.keyboard.press("Escape")

            # --- BƯỚC 6: PHÂN LOẠI FILE ---
            organize_downloaded_files()

            print("\n" + "="*60)
            print("🌟 TẤT CẢ TÁC VỤ ĐÃ HOÀN THÀNH XUẤT SẮC! 🌟")
            print(f"🎬 Video/Audio tại: {VIDEO_SAVE_PATH}")
            print(f"📸 Hình ảnh tại: {IMAGE_SAVE_PATH}")
            print("="*60)
            
            input("\n👉 NHẤN [ENTER] LẦN CUỐI ĐỂ ĐÓNG TRÌNH DUYỆT...")

        except Exception as e:
            print(f"❌ Lỗi hệ thống: {e}")
        
        finally:
            print("\n--- Kết thúc phiên làm việc ---")
            if context:
                context.close()

if __name__ == "__main__":
    run_automation()