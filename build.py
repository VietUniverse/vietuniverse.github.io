# build.py
import os
import glob
from pathlib import Path
import shutil

# --- Cấu hình ---
ARTICLES_DIR = 'articles'
OUTPUT_DIR = 'public'
TEMPLATE_DIR = 'templates'
TEMPLATE_FILE = os.path.join(TEMPLATE_DIR, 'template.html')
# Thư mục con trong 'public' để chứa hình ảnh đã sao chép
OUTPUT_IMAGES_DIR = os.path.join(OUTPUT_DIR, 'images')

def setup_output_dirs():
    """Tạo các thư mục output nếu chưa tồn tại."""
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    Path(OUTPUT_IMAGES_DIR).mkdir(exist_ok=True)
    print(f"Các thư mục '{OUTPUT_DIR}' và '{OUTPUT_IMAGES_DIR}' đã sẵn sàng.")

def get_article_dirs():
    """Lấy danh sách tất cả các thư mục bài viết và sắp xếp theo tên."""
    # Lấy tất cả các mục trong ARTICLES_DIR và chỉ giữ lại các thư mục
    article_dirs = [d for d in glob.glob(os.path.join(ARTICLES_DIR, '*')) if os.path.isdir(d)]
    article_dirs.sort()
    return article_dirs

def build_navigation(article_dirs, current_dir_path=None):
    """Tạo mã HTML cho menu điều hướng từ tên các thư mục."""
    nav_html = '<ul>\n'
    for article_path in article_dirs:
        dir_name = Path(article_path).name
        html_file_name = f"{dir_name}.html"
        
        is_current = (current_dir_path and Path(current_dir_path).name == dir_name)
        class_current = ' class="current"' if is_current else ''
        
        # Chuyển tên thư mục thành tiêu đề dễ đọc
        display_title = dir_name.replace("-", " ").title()
        nav_html += f'    <li><a href="{html_file_name}"{class_current}>{display_title}</a></li>\n'
    nav_html += '</ul>'
    return nav_html

def build_pages(article_dirs):
    """Xây dựng các trang HTML từ các thư mục bài viết."""
    if not article_dirs:
        print("Không tìm thấy thư mục bài viết nào trong 'articles'.")
        # Xử lý trường hợp không có bài viết (tương tự như trước)
        return

    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template_content = f.read()

    for article_dir in article_dirs:
        dir_name = Path(article_dir).name
        
        # Tìm file content.txt và file ảnh trong thư mục
        content_file = os.path.join(article_dir, 'content.txt')
        image_files = glob.glob(os.path.join(article_dir, '*.png')) + \
                      glob.glob(os.path.join(article_dir, '*.jpg')) + \
                      glob.glob(os.path.join(article_dir, '*.jpeg'))

        if not os.path.exists(content_file):
            print(f"Cảnh báo: Bỏ qua thư mục '{dir_name}' vì không tìm thấy 'content.txt'.")
            continue

        # Đọc nội dung từ content.txt
        with open(content_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            title = lines[0].strip()
            content_html = ''.join(f'<p>{line.strip()}</p>' for line in lines[1:] if line.strip())

        # Xử lý hình ảnh nếu có
        image_html = ''
        if image_files:
            image_path = image_files[0] # Lấy ảnh đầu tiên tìm thấy
            image_name = Path(image_path).name
            
            # Sao chép file ảnh vào thư mục public/images
            shutil.copy(image_path, os.path.join(OUTPUT_IMAGES_DIR, image_name))
            
            # Tạo thẻ HTML cho ảnh
            image_html = f'<img src="images/{image_name}" alt="Đề bài - {title}">'
            print(f"Đã xử lý ảnh: {image_name} cho bài viết '{dir_name}'")

        # Xây dựng trang
        nav_html = build_navigation(article_dirs, article_dir)
        page_content = template_content.replace('{{NAVIGATION}}', nav_html)
        page_content = page_content.replace('{{TITLE}}', title)
        page_content = page_content.replace('{{IMAGE_HTML}}', image_html)
        page_content = page_content.replace('{{CONTENT}}', content_html)

        # Ghi ra file HTML
        output_path = os.path.join(OUTPUT_DIR, f"{dir_name}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(page_content)
        print(f"Đã xây dựng trang: {output_path}")

    # Tạo file index.html trỏ đến bài viết đầu tiên
    first_article_dir_name = Path(article_dirs[0]).name
    shutil.copy(os.path.join(OUTPUT_DIR, f"{first_article_dir_name}.html"), os.path.join(OUTPUT_DIR, 'index.html'))
    print(f"Đã tạo trang index.html, trỏ tới bài '{first_article_dir_name}'.")

if __name__ == "__main__":
    print("--- Bắt đầu quá trình xây dựng website (phiên bản có hình ảnh) ---")
    setup_output_dirs()
    article_directories = get_article_dirs()
    build_pages(article_directories)
    print("--- Quá trình xây dựng hoàn tất! ---")
