#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成目录索引页面
在指定目录及其所有子目录中生成 index.html 文件
"""

import os
import sys
import html
from pathlib import Path
from datetime import datetime

# HTML模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>目录索引: {title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            padding: 30px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eaeaea;
        }}
        
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 28px;
        }}
        
        .path-info {{
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 20px;
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
        }}
        
        .up-link {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 8px 20px;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s ease;
            font-weight: 500;
            margin-bottom: 20px;
        }}
        
        .up-link:hover {{
            background: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        }}
        
        .content-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        
        .section {{
            margin-bottom: 30px;
        }}
        
        .section-title {{
            font-size: 20px;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
            display: flex;
            align-items: center;
        }}
        
        .section-title i {{
            margin-right: 10px;
            font-size: 18px;
        }}
        
        .file-list, .folder-list {{
            list-style: none;
        }}
        
        .file-list li, .folder-list li {{
            margin-bottom: 8px;
            transition: all 0.3s ease;
        }}
        
        .file-list li:hover, .folder-list li:hover {{
            transform: translateX(5px);
        }}
        
        .file-list a, .folder-list a {{
            display: flex;
            align-items: center;
            padding: 12px 15px;
            background: #f8f9fa;
            border-radius: 8px;
            color: #333;
            text-decoration: none;
            transition: all 0.3s ease;
            border-left: 4px solid transparent;
        }}
        
        .folder-list a {{
            border-left-color: #3498db;
        }}
        
        .file-list a {{
            border-left-color: #2ecc71;
        }}
        
        .file-list a:hover, .folder-list a:hover {{
            background: #e8f4fc;
            transform: translateX(5px);
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        }}
        
        .file-icon, .folder-icon {{
            margin-right: 12px;
            font-size: 20px;
        }}
        
        .file-icon {{ color: #2ecc71; }}
        .folder-icon {{ color: #3498db; }}
        
        .file-info {{
            font-size: 12px;
            color: #95a5a6;
            margin-left: auto;
            text-align: right;
        }}
        
        .stats {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        
        .stat-item {{
            text-align: center;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
        }}
        
        .stat-number {{
            font-size: 24px;
            font-weight: bold;
            color: #3498db;
        }}
        
        .stat-label {{
            font-size: 14px;
            color: #7f8c8d;
            margin-top: 5px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eaeaea;
            color: #95a5a6;
            font-size: 13px;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            
            .content-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        /* 文件类型颜色 */
        .pdf {{ color: #e74c3c; }}
        .image {{ color: #9b59b6; }}
        .text {{ color: #1abc9c; }}
        .archive {{ color: #f39c12; }}
        .code {{ color: #3498db; }}
        .document {{ color: #2ecc71; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📁 目录索引</h1>
            <div class="path-info">
                <strong>路径:</strong> {current_path}<br>
                <strong>生成时间:</strong> {generation_time}
            </div>
            
            {up_link}
        </div>
        
        <div class="content-grid">
            {content}
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{folder_count}</div>
                <div class="stat-label">📁 文件夹数量</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{file_count}</div>
                <div class="stat-label">📄 文件数量</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{total_size}</div>
                <div class="stat-label">💾 总大小</div>
            </div>
        </div>
        
        <div class="footer">
            自动生成于 {generation_time} | 共 {total_items} 个项目
        </div>
    </div>
</body>
</html>
"""

def format_file_size(size_in_bytes):
    """将文件大小转换为可读格式"""
    if size_in_bytes < 1024:
        return f"{size_in_bytes}B"
    elif size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes/1024:.1f}KB"
    elif size_in_bytes < 1024 * 1024 * 1024:
        return f"{size_in_bytes/(1024*1024):.1f}MB"
    else:
        return f"{size_in_bytes/(1024*1024*1024):.1f}GB"

def get_file_type(filename):
    """根据扩展名确定文件类型"""
    ext = os.path.splitext(filename)[1].lower()
    
    # 图片文件
    image_exts = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff']
    # 文档文件
    doc_exts = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx']
    # 代码文件
    code_exts = ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.go', '.rs']
    # 文本文件
    text_exts = ['.txt', '.md', '.json', '.xml', '.yaml', '.yml', '.csv', '.ini', '.conf']
    # 压缩文件
    archive_exts = ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2']
    
    if ext in image_exts:
        return "image", "🖼️"
    elif ext in doc_exts:
        return "document", "📄"
    elif ext in code_exts:
        return "code", "💻"
    elif ext in text_exts:
        return "text", "📝"
    elif ext in archive_exts:
        return "archive", "📦"
    elif ext == '.pdf':
        return "pdf", "📕"
    else:
        return "file", "📎"

def generate_index_html(directory, base_dir=None):
    """为指定目录生成 index.html 文件"""
    if base_dir is None:
        base_dir = directory
    
    try:
        # 获取当前目录的相对路径
        current_rel_path = os.path.relpath(directory, base_dir)
        if current_rel_path == '.':
            current_rel_path = ''
        
        # 获取所有条目
        entries = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            entries.append((item, item_path))
        
        # 分离文件夹和文件
        folders = []
        files = []
        total_size = 0
        
        for name, path in entries:
            if name.startswith('.'):
                continue  # 跳过隐藏文件
            
            if os.path.isdir(path):
                folders.append((name, path))
            else:
                if name.lower() == 'index.html':
                    continue  # 跳过 index.html 文件本身
                
                file_size = os.path.getsize(path)
                total_size += file_size
                files.append((name, path, file_size))
        
        # 排序：文件夹在前，按名称排序
        folders.sort(key=lambda x: x[0].lower())
        files.sort(key=lambda x: x[0].lower())
        
        # 准备内容
        content_parts = []
        
        # 文件夹部分
        if folders:
            folder_items = []
            for name, path in folders:
                # 为子目录生成索引
                generate_index_html(path, base_dir)
                
                folder_items.append(f"""
                    <li>
                        <a href="{html.escape(name)}/index.html">
                            <span class="folder-icon">📁</span>
                            <span>{html.escape(name)}</span>
                        </a>
                    </li>
                """)
            
            content_parts.append(f"""
                <div class="section">
                    <div class="section-title">
                        <span class="folder-icon">📁</span> 文件夹
                    </div>
                    <ul class="folder-list">
                        {''.join(folder_items)}
                    </ul>
                </div>
            """)
        
        # 文件部分
        if files:
            file_items = []
            for name, path, size in files:
                file_type, file_icon = get_file_type(name)
                size_str = format_file_size(size)
                encoded_name = html.escape(name)
                
                file_items.append(f"""
                    <li>
                        <a href="{encoded_name}" class="{file_type}">
                            <span class="file-icon">{file_icon}</span>
                            <span>{encoded_name}</span>
                            <div class="file-info">
                                {size_str}<br>
                                {file_type}
                            </div>
                        </a>
                    </li>
                """)
            
            content_parts.append(f"""
                <div class="section">
                    <div class="section-title">
                        <span class="file-icon">📄</span> 文件
                    </div>
                    <ul class="file-list">
                        {''.join(file_items)}
                    </ul>
                </div>
            """)
        
        # 生成返回上一级的链接
        up_link = ''
        if current_rel_path:  # 如果不是根目录
            parent_path = os.path.dirname(current_rel_path)
            if parent_path:
                up_link = f'<a href="../index.html" class="up-link">⬆️ 返回上一级</a>'
            else:
                up_link = f'<a href="index.html" class="up-link">⬆️ 返回根目录</a>'
        
        # 计算统计信息
        folder_count = len(folders)
        file_count = len(files)
        total_items = folder_count + file_count
        
        # 生成HTML
        html_content = HTML_TEMPLATE.format(
            title=os.path.basename(directory) if current_rel_path else "根目录",
            current_path=directory,
            generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            up_link=up_link,
            content=''.join(content_parts),
            folder_count=folder_count,
            file_count=file_count,
            total_size=format_file_size(total_size),
            total_items=total_items
        )
        
        # 写入文件
        index_path = os.path.join(directory, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ 生成: {index_path}")
        return True
        
    except Exception as e:
        print(f"✗ 错误 ({directory}): {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("📁 目录索引生成器")
    print("=" * 60)
    
    # 获取当前目录
    current_dir = os.getcwd()
    print(f"工作目录: {current_dir}")
    
    # 确认操作
    response = input("\n是否要为当前目录及其所有子目录生成索引？(y/n): ")
    if response.lower() != 'y':
        print("操作已取消")
        return
    
    print("\n正在生成索引...")
    print("-" * 60)
    
    # 生成索引
    success = generate_index_html(current_dir)
    
    if success:
        print("-" * 60)
        print("✅ 索引生成完成！")
        print(f"📁 主索引文件: {os.path.join(current_dir, 'index.html')}")
        print(f"🔗 可用浏览器打开查看目录结构")
    else:
        print("❌ 索引生成过程中出现错误")

if __name__ == "__main__":
    main()
