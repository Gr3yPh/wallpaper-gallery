import os
import urllib.parse
from datetime import datetime

# ================= 配置常量 =================
THEME_COLOR = "#66CCFF"
BG_IMAGE_PATH = "/luotianyi/luotianyi-12th-byTID.jpg"
REPO_URL = "https://github.com/Gr3yPh/wallpaper-gallery"
AUTHOR = "魇珩Gr3yPh4ntom"
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}

ICON_MAP = {
    'folder': 'fas fa-folder',
    'back': 'fas fa-arrow-left'
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gallery of {current_dir}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: url('{bg_path}') no-repeat center center fixed;
            background-size: cover;
            min-height: 100vh;
            color: #333;
        }}
        
        /* 顶部导航栏区域 */
        .header-bar {{
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            padding: 15px 20px;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.3);
        }}
        
        h1 {{ margin: 0; font-size: 1.2rem; color: #333; }}
        .nav-link {{
            text-decoration: none;
            color: {color};
            font-weight: bold;
            padding: 5px 10px;
            background: rgba(255,255,255,0.5);
            border-radius: 8px;
        }}

        /* 宫格布局容器 */
        .gallery-container {{
            padding: 20px;
            display: grid;
            /* 自适应宫格：最小200px，自动填充 */
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }}

        /* 文件夹样式 */
        .folder-card {{
            background: rgba(255, 255, 255, 0.5);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            text-decoration: none;
            color: #333;
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 10px;
            border: 1px solid rgba(255,255,255,0.3);
        }}
        .folder-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            background: rgba(255, 255, 255, 0.8);
        }}
        .folder-card i {{ font-size: 2rem; color: #FFC107; }}

        /* 图片卡片样式 */
        .img-card {{
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            aspect-ratio: 1 / 1; /* 保持正方形 */
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            cursor: pointer;
        }}
        .img-card img {{
            width: 100%;
            height: 100%;
            object-fit: cover; /* 关键：裁剪适应宫格，不拉伸 */
            transition: transform 0.3s;
        }}
        .img-card:hover img {{
            transform: scale(1.1);
        }}

        /* 全屏查看遮罩 */
        .lightbox {{
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.9);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            cursor: zoom-out;
        }}
        .lightbox img {{
            max-width: 90%;
            max-height: 90%;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }}
        
        footer {{
            text-align: center;
            color: white;
            padding: 20px;
            text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        }}
    </style>
</head>
<body>

    <div class="header-bar">
        <h1><i class="fas fa-images"></i> {current_dir}</h1>
        {back_link}
    </div>

    <div class="gallery-container">
        {items}
    </div>

    <div class="lightbox" id="lightbox" onclick="closeLightbox()">
        <img src="" id="lightbox-img" alt="Full view">
    </div>

    <footer>
        Copyright © {year} {author} | <a href="{repo_url}" target="_blank" style="color:white">Source</a>
    </footer>

    <script>
        function openLightbox(imgSrc) {{
            const lightbox = document.getElementById('lightbox');
            const lightboxImg = document.getElementById('lightbox-img');
            lightboxImg.src = imgSrc;
            lightbox.style.display = 'flex';
        }}

        function closeLightbox() {{
            document.getElementById('lightbox').style.display = 'none';
        }}
    </script>
</body>
</html>
"""

def generate_indices(root_dir):
    abs_root = os.path.abspath(root_dir)
    current_year = datetime.now().year
    script_name = os.path.basename(__file__)

    for current_path, dirs, files in os.walk(abs_root):
        if '.git' in dirs: dirs.remove('.git')
        if 'index.html' in files: files.remove('index.html')

        items_html = []
        
        # 1. 文件夹处理
        for d in sorted(dirs):
            if d.startswith('.'): continue
            link = urllib.parse.quote(d + '/')
            items_html.append(
                f'<a href="{link}" class="folder-card">'
                f'<i class="{ICON_MAP["folder"]}"></i>'
                f'<div>{d}</div>'
                f'</a>'
            )

        # 2. 图片处理 (隐藏文件名，纯预览)
        for f in sorted(files):
            if f == script_name or f.startswith('.'): continue
            
            ext = os.path.splitext(f)[1].lower()
            if ext not in IMAGE_EXTENSIONS: continue

            link = urllib.parse.quote(f)
            # 使用 JS 的 onclick 实现全屏点击
            item_html = (
                f'<div class="img-card" onclick="openLightbox(\'{link}\')">'
                f'<img src="{link}" alt="{f}" loading="lazy">'
                f'</div>'
            )
            items_html.append(item_html)

        # 3. 导航处理
        back_link = ""
        if current_path != abs_root:
            back_link = f'<a href="../" class="nav-link"><i class="{ICON_MAP["back"]}"></i> 返回</a>'

        rel_path = os.path.relpath(current_path, abs_root)
        display_path = "根目录" if rel_path == "." else rel_path.replace(os.sep, ' / ')

        output_file = os.path.join(current_path, "index.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(HTML_TEMPLATE.format(
                current_dir=display_path,
                bg_path=BG_IMAGE_PATH,
                color=THEME_COLOR,
                back_link=back_link,
                items="".join(items_html),
                year=current_year,
                author=AUTHOR,
                repo_url=REPO_URL
            ))

if __name__ == "__main__":
    generate_indices(".")
    print("宫格画廊生成完毕！")
