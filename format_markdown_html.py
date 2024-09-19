from img import process_markdown
from table import table_to_html
from format_table import format_all_table
import os
import shutil

def run_program(input_file, img_list, table_list, last_format_img):
    # 获取输入文件的目录
    input_dir = os.path.dirname(input_file)

    # 设置复制后文件的路径及名称为 "README_copy.md"
    input_file_copy = os.path.join(input_dir, "README_copy.md")

    # 检查 "README_copy.md" 是否存在
    if not os.path.exists(input_file_copy):
        # 复制文件并重命名
        shutil.copy(input_file, input_file_copy)
        print(f"文件已复制并重命名为: {input_file_copy}")
    else:
        print(f"文件 {input_file_copy} 已存在，跳过复制操作")

    process_markdown(input_file, img_list)

    for lis in table_list:
        if lis == 1:
            print("执行功能1:将文档中的markdown表格转换为html表格")
            table_to_html(input_file)
        elif lis == 2:
            print("执行功能2:格式化所有的html表格")
            format_all_table(input_file)
    if last_format_img:
        process_markdown(input_file, [2])
    print("已完成格式化文档")

if __name__ == "__main__":
    last_format_img = True
    # 用户只需提供输入文件路径，输出文件自动生成
    # 1 将Markdown格式的图片转换为HTML格式
    # 2 格式化<img>为alt，src，ma-width
    # 3 删除images中多余的图片
    # 4 将 'images' 重命名为 'images' 并更新图片路径
    img_list = [1, 2, 3, 4]

    # 1 将所有markdown表格转换为html表格
    # 2 格式化所有html表格
    table_list = [1, 2]

    input_file = r"F:\Desktop\ed-docs\docs\zh\hmi3020-101c\ds\README.md"
    # 检查文件是否存在
    if not os.path.isfile(input_file):
        print(f"文件 {input_file} 不存在，请检查路径。")
    else:
        # 调用主程序处理
        run_program(input_file, img_list, table_list, last_format_img)
