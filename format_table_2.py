import re

# 删除不必要的空行，并为表格添加缩进格式
def format_table_html(content):
    # 定义标签及其缩进量的列表
    indentation_levels = {
        "<table": 0,
        "<thead": 2,
        "</thead": 2,
        "<tbody": 2,
        "</tbody": 2,
        "<tr": 4,
        "</tr": 4,
        "<th": 6,
        "<td": 6,
    }

    # 定义正则表达式来确保标签在独立的行
    def ensure_single_line_tag(line):
        line = re.sub(r">\s*<", ">\n<", line)  # 确保每个标签之间有换行符
        return line.strip()

    formatted_lines = []
    in_table = False

    for line in content.splitlines():
        stripped_line = line.strip()

        # 进入表格时，标记开始处理表格内的标签
        if stripped_line.startswith("<table"):
            in_table = True
            formatted_lines.append(ensure_single_line_tag(stripped_line))  # <table> 不缩进

        # 离开表格时，标记结束处理表格内的标签
        elif stripped_line.startswith("</table>"):
            formatted_lines.append(ensure_single_line_tag(stripped_line))  # </table> 不缩进
            in_table = False

        # 对表格的标签（thead, tbody, tr, th, td）处理缩进
        elif in_table:
            if stripped_line:  # 忽略空行
                tag_found = False
                for tag, indent in indentation_levels.items():
                    if stripped_line.startswith(tag):
                        # 为匹配的标签添加缩进
                        content_inside_tag = ensure_single_line_tag(stripped_line)
                        formatted_lines.append(" " * indent + content_inside_tag)
                        tag_found = True
                        break
                if not tag_found:
                    # 默认缩进 2 个空格
                    formatted_lines.append("  " + stripped_line)

        # 对表格外的部分不做处理，保持原样
        else:
            formatted_lines.append(line)

    return "\n".join(formatted_lines)

# 处理 Markdown 文件，直接覆盖写入原文件
def process_markdown_file_in_place2(input_path):
    try:
        # 读取输入文件内容
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 只格式化表格 HTML，添加缩进
        processed_content = format_table_html(content)

        # 覆盖写回输入文件
        with open(input_path, 'w', encoding='utf-8') as file:
            file.write(processed_content)

        print(f"文件已处理完成第3步，保存到: {input_path}")
    except Exception as e:
        print(f"处理文件时出错: {e}")

# # 示例调用
# input_path = 'output.md'  # 输入的 Markdown 文件
# process_markdown_file_in_place2(input_path)
