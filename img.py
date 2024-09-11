import os
import re
import shutil

# 读取文件内容
def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 写入文件内容
def write_file(file_path, content):
    """将内容写回文件"""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# 功能1: 将Markdown格式的图片转换为HTML格式
def convert_md_images_to_html(markdown_text):
    """将Markdown中的图片转换为HTML格式并格式化为src, alt, style"""
    md_image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    def replace_with_html(match):
        alt_text = match.group(1) or 'image'
        src = match.group(2)
        return f'<img src="{src}" alt="{alt_text}" style="max-width: 50%;">'

    return re.sub(md_image_pattern, replace_with_html, markdown_text)

# 功能2: 将所有<img>标签格式化为src, alt, style
def format_img_tags_in_html(markdown_text):
    """检测所有<img>标签并格式化为src, alt, style"""
    img_tag_pattern = r'<img\s+([^>]*?)>'

    def replace_img_tag(match):
        attributes = match.group(1)
        src_match = re.search(r'src="([^"]+)"', attributes)
        alt_match = re.search(r'alt="([^"]*)"', attributes)

        src = src_match.group(1) if src_match else '#'
        alt = alt_match.group(1) if alt_match else 'image'

        return f'<img src="{src}" alt="{alt}" style="max-width: 50%;">'

    return re.sub(img_tag_pattern, replace_img_tag, markdown_text)

# 功能3: 统计Images目录和文档中的图片列表，并删除列表1中多余的图片
def cleanup_images_in_directory(input_file, images_dir):
    """删除Images目录中不存在于文档中的图片"""
    markdown_text = read_file(input_file)

    # 获取Images目录中的图片列表 (列表1)
    list1 = set(os.listdir(images_dir))

    # 获取文档中图片的名称 (列表2)
    list2 = set()
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)|<img\s+[^>]*?src="([^"]+)"'

    def extract_image_name(match):
        if match.group(2):  # Markdown格式的图片
            src = match.group(2)
            if src.endswith('.png'):
                list2.add(os.path.basename(src))
        elif match.group(3):  # <img>标签的图片
            src = match.group(3)
            if src.endswith('.png'):
                list2.add(os.path.basename(src))

    re.findall(image_pattern, markdown_text, flags=re.IGNORECASE)
    re.sub(image_pattern, extract_image_name, markdown_text)

    # 删除只在列表1中存在，而不在列表2中的图片
    for image in list1:
        if image not in list2:
            image_path = os.path.join(images_dir, image)
            if os.path.isfile(image_path):
                os.remove(image_path)
                print(f'删除图片: {image}')

# 功能4: 将目录 'Images' 重命名为 'images' 并修正文档中的图片路径
def rename_images_directory_and_update_paths(input_file, images_dir):
    """如果目录 'Images' 存在，将其重命名为 'images' 并更新文档中的图片路径"""
    markdown_text = read_file(input_file)
    images_dir_lower = os.path.join(os.path.dirname(images_dir), 'images')

    if os.path.isdir(images_dir):
        # 重命名目录 'Images' 为 'images'
        os.rename(images_dir, images_dir_lower)
        print(f"重命名目录: {images_dir} -> {images_dir_lower}")

        # 替换文档中的图片路径 'Images' -> 'images'
        # 处理相对路径，包含 ./Images/ 和 /Images/ 两种情况
        markdown_text = re.sub(r'src=["\']\./Images/', 'src="./images/', markdown_text)
        markdown_text = re.sub(r'src=["\']/Images/', 'src="/images/', markdown_text)
        write_file(input_file, markdown_text)
        print(f"文档中的图片路径已更新: './Images/' -> './images/'")

# 从input_file生成Images目录路径
def get_images_directory(input_file):
    """根据input_file的路径生成Images或images目录路径"""
    base_dir = os.path.dirname(input_file)
    images_dir_upper = os.path.join(base_dir, 'Images')
    images_dir_lower = os.path.join(base_dir, 'images')

    # 检测 'Images' 或 'images' 是否存在
    if os.path.isdir(images_dir_upper):
        return images_dir_upper
    elif os.path.isdir(images_dir_lower):
        return images_dir_lower
    else:
        print("Error: 找不到 'Images' 或 'images' 目录")
        return None

# 主函数：根据需要执行的功能顺序
def process_markdown(input_file, operations):
    """按顺序执行指定的功能"""
    markdown_text = read_file(input_file)

    # 获取图片目录
    images_dir = get_images_directory(input_file)
    if not images_dir:
        return  # 如果没有找到有效的图片目录，则退出

    for operation in operations:
        if operation == 1:
            print("执行功能1: 将Markdown图片转换为HTML格式")
            markdown_text = convert_md_images_to_html(markdown_text)
        elif operation == 2:
            print("执行功能2: 格式化<img>标签")
            markdown_text = format_img_tags_in_html(markdown_text)
        elif operation == 3:
            print("执行功能3: 清理Images目录中多余的图片")
            cleanup_images_in_directory(input_file, images_dir)
        elif operation == 4:
            print("执行功能4: 将 'Images' 目录重命名为 'images' 并更新图片路径")
            rename_images_directory_and_update_paths(input_file, images_dir)

    write_file(input_file, markdown_text)
    print(f"文件已处理并保存: {input_file}")

# 调用主函数
input_file = r'F:\Desktop\ed-docs-new-style\docs\zh\ipc2400\ds\README.md'

# 1 将Markdown格式的图片转换为HTML格式
# 2 格式化<img>为alt，src，ma-width
# 3 删除images中多余的图片
# 4 将 'Images' 重命名为 'images' 并更新图片路径
operations = [1, 2]  # 根据需要调整执行顺序，例如 [3, 2, 1] 或 [1] 或其他组合

process_markdown(input_file, operations)
