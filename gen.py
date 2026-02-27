import os
import urllib.parse
from datetime import datetime

# ================= 配置常量 =================
THEME_COLOR = "#66CCFF"
BG_IMAGE_PATH = "/luotianyi/luo-tianyi-12th-byTID.jpg"
REPO_URL = "https://github.com/Gr3yPh/wallpaper-gallery"
AUTHOR = "魇珩Gr3yPh4ntom"
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}

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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>Index of {current_dir}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {{
            margin: 0;
            padding: 20px 10px;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: url('{bg_path}') no-repeat center center fixed;
            background-size: cover;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-sizing: border-box;
        }}
        .container {{
            width: 100%;
            max-width: 900px;
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(15px) saturate(160%);
            -webkit-backdrop-filter: blur(15px) saturate(160%);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            box-sizing: border-box;
        }}
        h1 {{
            color: {color};
            font-weight: 400;
            font-size: 1.5rem;
            margin-top: 0;
            border-bottom: 2px solid rgba(102, 204, 255, 0.3);
            padding-bottom: 15px;
            word-break: break-all;
        }}
        .nav-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin: 10px 0 20px 0;
            text-decoration: none;
            color: #444;
            font-weight: 600;
            padding: 8px 15px;
            background: rgba(255,255,255,0.5);
            border-radius: 10px;
        }}
        ul {{ list-style: none; padding: 0; margin: 0; }}
        li {{
            margin: 10px 0;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.3);
            overflow: hidden;
        }}
        a.item-link {{
            padding: 15px;
            text-decoration: none;
            color: #333;
            display: block;
        }}
        .item-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1rem;
            line-height: 1.4;
        }}
        .preview-img {{
            display: block;
            width: 100%; 
            max-width: 400px;
            height: auto;
            margin-top: 12px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            background: #eee;
        }}
        footer {{
            margin-top: 30px;
            text-align: center;
            color: white;
            text-shadow: 0 1px 3px rgba(0,0,0,0.5);
            font-size: 0.85rem;
            padding: 15px;
            width: 90%;
            word-break: break-all;
        }}
        @media (max-width: 600px) {{
            .container {{ padding: 15px; border-radius: 15px; }}
            h1 {{ font-size: 1.2rem; }}
            .preview-img {{ max-width: 100%; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1><i class="fas fa-layer-group"></i> {current_dir}</h1>
        {back_link}
        <ul>
            {items}
        </ul>
    </div>
    <footer>
        Copyright © {year} {author}<br>
        Repo: <a href="{repo_url}" target="_blank" style="color:{color}">Source Code</a>
    </footer>
</body>
</html>
"""

def generate_indices(root_dir):
    abs_root = os.path.abspath(root_dir)
    current_year = datetime.now().year
    script_name = os.path.basename(__file__)

    for current_path, dirs, files in os.walk(abs_root):
        if '.git' in dirs:
            dirs.remove('.git')
        
        if 'index.html' in files:
            files.remove('index.html')

        items_html = []
        
        for d in sorted(dirs):
            if d.startswith('.'): continue
            link = urllib.parse.quote(d + '/')
            items_html.append(
                f'<li><a class="item-link" href="{link}">'
                f'<div class="item-header"><i class="{ICON_MAP["folder"]} fa-fw"></i> {d}/</div>'
                f'</a></li>'
            )

        for f in sorted(files):
            if f == script_name or f.startswith('.'):
                continue

            link = urllib.parse.quote(f)
            ext = os.path.splitext(f)[1].lower()
            icon = ICON_MAP["image"] if ext in IMAGE_EXTENSIONS else ICON_MAP["file"]

            item_html = (
                f'<li><a class="item-link" href="{link}">'
                f'<div class="item-header"><i class="{icon} fa-fw"></i> {f}</div>'
            )
            if ext in IMAGE_EXTENSIONS:
                item_html += f'<img src="{link}" class="preview-img" alt="{f}" loading="lazy">'
            
            item_html += '</a></li>'
            items_html.append(item_html)

        back_link = ""
        if current_path != abs_root:
            back_link = f'<a href="../" class="nav-link"><i class="{ICON_MAP["back"]}"></i> 返回上级</a>'

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
    print("Generation task complete.")
