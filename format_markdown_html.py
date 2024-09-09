import format_table
import format_table_2
import img_html
import table_to_html
import os
import shutil


def run_program(input_file):
    # 自动生成输出文件路径
    output_file = input_file.replace(".md", "_processed.md")

    temp_file = 'temp_output.md'  # 用于临时存储中间结果的文件
    shutil.copy(input_file, temp_file)  # 先拷贝输入文件到临时文件

    # 按照顺序执行 1, 2, 3, 4 步
    print("执行第1步：转换 Markdown 表格为 HTML 表格")
    table_to_html.process_markdown_file(temp_file, temp_file)

    print("执行第2步：转换 Markdown 图片为 HTML 图片")
    img_html.convert_md_images_to_html_in_place(temp_file)

    print("执行第3步：运行 format_table 表格格式化")
    format_table.process_markdown_file_in_place(temp_file)

    print("执行第4步：运行 format_table_2 表格格式化")
    format_table_2.process_markdown_file_in_place2(temp_file)

    # 最终结果写入输出文件
    shutil.move(temp_file, output_file)
    print(f"所有操作已完成，最终结果写入 {output_file}")


if __name__ == "__main__":
    # 用户只需提供输入文件路径，输出文件自动生成
    input_file = input("请输入要处理的 Markdown 文件路径: ").strip()

    # 检查文件是否存在
    if not os.path.isfile(input_file):
        print(f"文件 {input_file} 不存在，请检查路径。")
    else:
        # 调用主程序处理
        run_program(input_file)
