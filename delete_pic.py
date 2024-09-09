import os
import re

# 读取MD文件中的图片引用路径
def get_images_from_md(md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # 使用正则表达式提取 <img> 标签中的图片路径
    img_pattern = r'<img[^>]+src=["\'](.*?)["\']'
    used_images = re.findall(img_pattern, content)
    return used_images, content

# 获取Images文件夹中的所有图片
def get_images_from_folder(images_folder):
    return os.listdir(images_folder)

# 删除未使用的图片，并打印删除的图片名
def delete_unused_images(images_folder, images_in_md, images_in_folder):
    images_in_md_basename = {os.path.splitext(os.path.basename(img))[0] for img in images_in_md}  # 获取文档中引用的图片名（不含扩展名）
    images_in_folder_basename = {os.path.splitext(img)[0] for img in images_in_folder}  # 获取文件夹中图片的基础名（不含扩展名）

    # 计算未使用的图片
    unused_images = images_in_folder_basename - images_in_md_basename  # 不在文档中引用的图片
    unused_images_full = [img for img in images_in_folder if os.path.splitext(img)[0] in unused_images]  # 获取未使用图片的完整文件名

    print("\n删除的图片名：")
    for unused_image in unused_images_full:
        print(unused_image)
        os.remove(os.path.join(images_folder, unused_image))
    return unused_images_full

# 修改图片名称：空格替换为'-'，中文翻译为英文，并打印修改结果
def rename_images(images_in_md, images_folder):
    rename_map = {}
    for img_path in images_in_md:
        img_name = os.path.basename(img_path)
        new_img_name = img_name

        # 替换空格为 '-'
        if ' ' in new_img_name:
            new_img_name = new_img_name.replace(' ', '-')

        # 检查并翻译中文名称
        if re.search(r'[\u4e00-\u9fff]', new_img_name):
            english_name = input(f"请输入图片 {new_img_name} 的英文名称：")
            new_img_name = english_name

        # 如果名称发生了变化，记录修改映射并打印修改信息
        if new_img_name != img_name:
            rename_map[img_name] = new_img_name
            old_image_path = os.path.join(images_folder, img_name)
            new_image_path = os.path.join(images_folder, new_img_name)
            if os.path.exists(old_image_path):
                os.rename(old_image_path, new_image_path)
                print(f"图片已修改：{img_name} -> {new_img_name}")  # 打印修改的图片名称

    return rename_map

# 更新MD文件中的图片路径
def update_md_content(content, rename_map):
    for old_name, new_name in rename_map.items():
        content = content.replace(old_name, new_name)
    return content

# 重命名Images文件夹为images
def rename_images_folder(images_folder):
    new_images_folder = images_folder.lower()
    if os.path.exists(images_folder):
        os.rename(images_folder, new_images_folder)
    return new_images_folder

# 更新MD文件中的路径 ./Images 替换为 ./images
def update_md_paths(content):
    return content.replace('./Images', './images')

# 写回MD文件
def write_md_file(md_file_path, content):
    with open(md_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# 主函数
def process_md_and_images(md_file_path):
    # 根据文档路径推断Images文件夹路径
    images_folder = os.path.join(os.path.dirname(md_file_path), 'Images')

    # 1. 读取MD文件中的图片引用路径（列表1）
    images_in_md, content = get_images_from_md(md_file_path)
    print("\n文档中引用的图片列表：")
    for img in images_in_md:
        print(os.path.basename(img))

    # 2. 读取Images文件夹中的所有图片（列表2）
    images_in_folder = get_images_from_folder(images_folder)
    print("\nImages文件夹中的图片列表：")
    for img in images_in_folder:
        print(img)

    # 3. 删除Images文件夹中未使用的图片
    delete_unused_images(images_folder, images_in_md, images_in_folder)

    # 4. 修改图片名称并打印修改情况
    rename_map = rename_images(images_in_md, images_folder)

    # 5. 更新MD文件中的图片路径
    content = update_md_content(content, rename_map)

    # 6. 重命名Images文件夹为images
    new_images_folder = rename_images_folder(images_folder)

    # 7. 修改MD文件中的 ./Images 为 ./images
    content = update_md_paths(content)

    # 8. 写回MD文件
    write_md_file(md_file_path, content)

    print("\n处理完成！")

# 调用主函数并提示用户输入文件路径
md_file_path = input("请输入文件路径: ")
process_md_and_images(md_file_path)
