import re

def convert_md_images_to_html_in_place(md_file_path):
    # 读取 Markdown 文件内容
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        content = md_file.readlines()

    # 正则表达式匹配 Markdown 图片语法 ![alt text](image url)，允许图片路径中的双斜杠
    md_image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    # 正则表达式匹配已有的 HTML img 标签，没有 style 或 width 属性
    html_image_pattern_without_maxwidth = (
        r'(<img\s+[^>]*src="([^"]+)"\s+alt="([^"]*)"(?![^>]*\b(width|max-width)\b)[^>]*>)'
    )

    # 替换为带有 max-width 的 img 标签，并确保 src 在前
    def add_maxwidth(match):
        src = match.group(2)  # 图片的 src
        alt = match.group(3)  # 图片的 alt
        # 返回的 img 标签中 src 在 alt 之前
        return f'<img src="{src}" alt="{alt}" style="max-width: 50%;">'

    # 替换内容
    new_content = []
    for line in content:
        # 1. 替换 Markdown 图片链接为 HTML 格式，并确保 src 在前
        new_line = re.sub(md_image_pattern, r'<img src="\2" alt="\1" style="max-width: 50%;">', line)

        # 2. 替换没有 max-width 或 width 的 img 标签，添加 max-width
        new_line = re.sub(html_image_pattern_without_maxwidth, add_maxwidth, new_line)

        new_content.append(new_line)

    # 将新的内容覆盖写回文件
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.writelines(new_content)

    print(f"完成第2步，已修改 {md_file_path} 文件中的图片链接为 HTML 格式，并保留所有格式和缩进。")

# 示例使用
# md_file = 'output.md'
# convert_md_images_to_html_in_place(md_file)
