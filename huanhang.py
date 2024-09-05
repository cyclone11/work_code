import re

def add_line_break_before_dash_and_hash(input_file):
    # 从输入文件读取内容
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 只在遇到 "- "（连字符加空格且不在行首）时换行
    formatted_content = re.sub(r'(?<!\n)- ', r'\n- ', content)

    # 删除两个 "- " 之间的换行符
    formatted_content = re.sub(r'\n(?=\s*- [^\n]*- )', '', formatted_content)

    # 将非行首的 # 放到下一行的开头，行首的 # 不做修改
    formatted_content = re.sub(r'(?<!^)(?<!\n)(#+)', r'\n\1', formatted_content, flags=re.MULTILINE)

    # 将 ![ 标记放到下一行
    formatted_content = re.sub(r'(?<!\n)(!\[)', r'\n\1', formatted_content)

    # 将结果写回源文件，覆盖原文件
    with open(input_file, 'w', encoding='utf-8') as file:
        file.write(formatted_content)


# 使用示例
input_file = r'F:\Desktop\Code\output.html'  # 源文件路径

add_line_break_before_dash_and_hash(input_file)
