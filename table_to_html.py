import re

def remove_bold_formatting(text):
    """
    移除文本中的 **加粗** 格式。
    """
    return re.sub(r'\*\*(.*?)\*\*', r'\1', text)

def convert_md_table_to_html(md_table):
    """
    将 Markdown 表格转换为 HTML 表格，并删除表头的加粗格式。
    """
    # 拆分表格行
    rows = [row.strip() for row in md_table.strip().split("\n") if row.strip()]

    # 提取表头和数据
    header = rows[0]  # 第一行是表头
    divider = rows[1]  # 第二行是分隔符
    data_rows = rows[2:]  # 其余的是表数据

    # 转换表头并删除加粗
    headers = [remove_bold_formatting(col.strip()) for col in header.split('|') if col.strip()]
    html_table = '<table>\n  <thead>\n    <tr>\n'
    for h in headers:
        html_table += f'      <th>{h}</th>\n'
    html_table += '    </tr>\n  </thead>\n  <tbody>\n'

    # 转换表格数据
    for row in data_rows:
        cols = [col.strip() for col in row.split('|') if col.strip()]
        html_table += '    <tr>\n'
        for col in cols:
            html_table += f'      <td>{col}</td>\n'
        html_table += '    </tr>\n'

    html_table += '  </tbody>\n</table>\n'
    return html_table

def process_markdown_file(input_file, output_file):
    """
    处理 Markdown 文件，将其中的 Markdown 表格转换为 HTML 表格，并将结果保存到输出文件。
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则表达式匹配 Markdown 表格
    md_table_pattern = re.compile(r'((?:\|.+\n)+)')  # 匹配连续的竖线表格

    # 找到所有 Markdown 表格并进行替换
    new_content = content
    matches = md_table_pattern.findall(content)

    for md_table in matches:
        html_table = convert_md_table_to_html(md_table)
        new_content = new_content.replace(md_table, html_table)

    # 将转换后的内容写入输出文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(new_content)
    print(f"完成，Markdown 表格已转换为 HTML 表格并写入 {output_file}")

# 示例使用，指定输入 Markdown 文件和输出文件
input_file = r'F:\Desktop\ed-docs-new-style\docs\zh\ipc2400\um\1-hardware\README.md'
output_file = "output.md"

# 调用函数，将 Markdown 表格转换为 HTML 表格，并保存到输出文件
process_markdown_file(input_file, output_file)
