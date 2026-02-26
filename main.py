import os
import shutil
import re
from playwright.sync_api import sync_playwright

# --- CẤU HÌNH ĐƯỜNG DẪN ---
FOLDER_PATH = r"C:\Users\ADMIN\Desktop\Github Fulll Project\NotebookLM-Automation\Documentss"
VIDEO_SAVE_PATH = r"C:\Users\ADMIN\Desktop\Github Fulll Project\NotebookLM-Automation\Video"
IMAGE_SAVE_PATH = r"C:\Users\ADMIN\Desktop\Github Fulll Project\NotebookLM-Automation\Images_NoteBookLM"
USER_DATA_DIR = r"C:\Users\ADMIN\Desktop\ChromeAuto"

# Khởi tạo thư mục nếu chưa có
for path in [VIDEO_SAVE_PATH, IMAGE_SAVE_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"📁 Đã chuẩn bị thư mục: {path}")

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

def run_automation():
    with sync_playwright() as p:
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

            # --- BƯỚC 1: TẠO NOTEBOOK MỚI ---
            print("🔍 Đang tìm nút tạo Notebook...")
            new_btn = page.locator("button:has-text('Tạo'), [role='button']:has-text('Tạo')").first
            new_btn.wait_for(state="visible", timeout=15000)
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
                video_card = page.locator("[aria-label*='Tổng quan bằng video']").last
                video_card.wait_for(state="visible", timeout=10000)
                video_card.click(force=True)

                create_confirm = page.locator("button:has-text('Tạo')").last
                create_confirm.wait_for(state="visible", timeout=5000)
                create_confirm.click(force=True)
                print("✅ Đã kích hoạt Render Video.")
            except Exception as e:
                print(f"⚠️ Không thể tự động bấm 'Tạo Video': {e}")

            page.wait_for_timeout(3000) # Nghỉ để UI cập nhật

            # 3.2 Tạo Bản đồ hoạ thông tin
            try:
                print("📊 Đang yêu cầu tạo 'Bản đồ hoạ thông tin'...")
                # Locator linh hoạt hơn để tránh lỗi timeout
                infographic_btn = page.locator("div[aria-label='Bản đồ hoạ thông tin'], [role='button']:has-text('Bản đồ hoạ thông tin')").last
                
                infographic_btn.scroll_into_view_if_needed()
                infographic_btn.click(force=True, timeout=5000)
                
                page.wait_for_timeout(1000)
                final_create_btn = page.locator("button:has-text('Tạo')").last
                if final_create_btn.is_visible():
                    final_create_btn.click(force=True)
                print("✅ Đã kích hoạt tạo Bản đồ hoạ thông tin.")
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
            context.close()

if __name__ == "__main__":
    run_automation()