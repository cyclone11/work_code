import re

def convert_md_images_to_html_in_place(md_file_path):
    # 读取 Markdown 文件内容
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        content = md_file.readlines()

    # 正则表达式匹配 Markdown 图片语法 ![alt text](image url)
    md_image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    # 正则表达式匹配已有的 HTML img 标签，并替换 zoom 属性为 max-width
    html_image_pattern = r'<img\s+src="([^"]+)"\s+alt="([^"]*)"\s+style="[^"]*zoom:[^;"]*;"[^>]*>'

    # 替换为 HTML 格式 <img src="image_url" alt="alt text" style="max-width: 50%;">
    html_image_replacement = r'<img src="\1" alt="\2" style="max-width:50%;">'

    # 替换内容，保留原来的格式和缩进
    new_content = []
    for line in content:
        # 替换 Markdown 图片链接为 HTML 格式
        new_line = re.sub(md_image_pattern, html_image_replacement, line)
        # 替换已有的 img 标签，并将 zoom 属性改为 max-width
        new_line = re.sub(html_image_pattern, html_image_replacement, new_line)
        new_content.append(new_line)

    # 将新的内容覆盖写回文件
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.writelines(new_content)

    print(f"已修改 {md_file_path} 文件中的图片链接为 HTML 格式，并保留所有格式和缩进。")

# 示例使用
md_file = r'F:\Desktop\ed-docs-new-style\docs\zh\hmi2020-070c\ds\README.md'

convert_md_images_to_html_in_place(md_file)
