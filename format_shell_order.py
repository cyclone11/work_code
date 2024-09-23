import re

def replace_asterisks_in_file(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 第一步：删除反引号之前的空格，直到遇到换行符或文件开头
    content = re.sub(r'(^|\n)\s+`', r'\1`', content)

    # 第二步：匹配并替换以 ` 开头并以 ` 结束的内容
    pattern = r'`([^`]*)`\n'
    modified_content = re.sub(pattern, r'```sh\n\1\n```', content)

    # 第三步：删除行首到 ```sh 之前的空格
    modified_content = remove_spaces_before_triple_backticks(modified_content)

    # 将修改后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)

    print(f"已修改文件: {file_path}")

def remove_spaces_before_triple_backticks(text):
    # 匹配行首到 ```sh 之前的空格并删除
    return re.sub(r'(^|\n)\s+```sh', r'\1```sh', text)

# 测试用例：输入文件路径
md_file_path = r"F:\Desktop\ed-docs\docs\zh\ipc2100\um\5-configuring-system\README.md"

replace_asterisks_in_file(md_file_path)
