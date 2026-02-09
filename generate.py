import os
import urllib.parse
from datetime import datetime

# 配置常量
THEME_COLOR = "#66CCFF"
BG_IMAGE_PATH = "/luotianyi/cloud-mirror.png"
REPO_URL = "https://github.com/Gr3yPh/wallpaper-gallery"
AUTHOR = "魇珩Gr3yPh4ntom"
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}

# Font Awesome 图标映射
ICON_MAP = {
    'folder': 'fas fa-folder',
    'image': 'fas fa-file-image',
    'file': 'fas fa-file-alt',
    'back': 'fas fa-arrow-left'
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index of {current_dir}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {{
            margin: 0;
            padding: 40px 20px;
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: url('{bg_path}') no-repeat center center fixed;
            background-size: cover;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .container {{
            width: 100%;
            max-width: 900px;
            background: rgba(255, 255, 255, 0.35);
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        }}
        h1 {{
            color: {color};
            font-weight: 300;
            margin-top: 0;
            border-bottom: 1px solid rgba(102, 204, 255, 0.3);
            padding-bottom: 15px;
            word-break: break-all;
        }}
        .nav-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 25px;
            text-decoration: none;
            color: #444;
            font-weight: 600;
            transition: color 0.3s;
        }}
        .nav-link:hover {{ color: {color}; }}
        
        ul {{ list-style: none; padding: 0; margin: 0; }}
        li {{
            margin: 8px 0;
            background: rgba(255, 255, 255, 0.4);
            border-radius: 12px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid transparent;
        }}
        li:hover {{
            transform: translateY(-2px);
            background: rgba(255, 255, 255, 0.7);
            border-color: {color};
            box-shadow: 0 5px 15px rgba(102, 204, 255, 0.2);
        }}
        
        a.item-link {{
            padding: 15px 20px;
            text-decoration: none;
            color: #333;
            display: flex;
            flex-direction: column;
        }}
        .item-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.05rem;
        }}
        .fa-folder {{ color: #FFCA28; }}
        .fa-file-image {{ color: {color}; }}
        .fa-file-alt {{ color: #999; }}
        
        .preview-img {{
            display: block;
            max-width: 100%;
            width: 320px;
            height: auto;
            margin-top: 15px;
            border-radius: 10px;
            border: 3px solid white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        footer {{
            margin-top: 40px;
            text-align: center;
            color: white;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            font-size: 0.9rem;
            line-height: 1.6;
            background: rgba(0, 0, 0, 0.2);
            padding: 15px 30px;
            border-radius: 50px;
            backdrop-filter: blur(5px);
        }}
        footer a {{ color: {color}; text-decoration: none; }}
        footer a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1><i class="fas fa-layer-group"></i> Index of {current_dir}</h1>
        {back_link}
        <ul>
            {items}
        </ul>
    </div>
    <footer>
        Copyright © {year} {author}<br>
        Repo Source: <a href="{repo_url}" target="_blank">{repo_url}</a>
    </footer>
</body>
</html>
"""

def generate_indices(root_dir):
    abs_root = os.path.abspath(root_dir)
    current_year = datetime.now().year

    for current_path, dirs, files in os.walk(abs_root):
        # 清理旧索引干扰
        if 'index.html' in files:
            files.remove('index.html')
            
        items_html = []
        
        # 文件夹
        for d in sorted(dirs):
            link = urllib.parse.quote(d + '/')
            items_html.append(
                f'<li><a class="item-link" href="{link}">'
                f'<div class="item-header"><i class="{ICON_MAP["folder"]}"></i> {d}/</div>'
                f'</a></li>'
            )

        # 文件
        for f in sorted(files):
            if f == os.path.basename(__file__): continue
            
            link = urllib.parse.quote(f)
            ext = os.path.splitext(f)[1].lower()
            
            icon = ICON_MAP["image"] if ext in IMAGE_EXTENSIONS else ICON_MAP["file"]
            
            item_html = (
                f'<li><a class="item-link" href="{link}">'
                f'<div class="item-header"><i class="{icon}"></i> {f}</div>'
            )
            
            if ext in IMAGE_EXTENSIONS:
                item_html += f'<img src="{link}" class="preview-img" alt="{f}" loading="lazy">'
            
            item_html += '</a></li>'
            items_html.append(item_html)

        # 返回上级
        back_link = ""
        if current_path != abs_root:
            back_link = f'<a href="../" class="nav-link"><i class="{ICON_MAP["back"]}"></i> 返回上级目录</a>'

        # 写入
        rel_path = os.path.relpath(current_path, abs_root)
        display_path = "/" if rel_path == "." else f" / {rel_path.replace(os.sep, ' / ')}"
        
        with open(os.path.join(current_path, "index.html"), "w", encoding="utf-8") as f:
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
    #print("✨ 洛天依主题索引文件生成完毕！(Font Awesome 已启用)")
