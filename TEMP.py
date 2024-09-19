from bs4 import BeautifulSoup
import os

def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 写入文件内容
def write_file(file_path, content):
    """将内容写回文件"""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def reorder_img_attributes(img):
    """重新排序img标签的属性，使src放在alt前面，并将alt设为src的文件名"""
    attrs = img.attrs
    # 获取 src 和 alt 属性
    src = attrs.get('src', '')
    new_img_tag = f'<img src="{src}"'
    new_img_tag += '>'

    return new_img_tag

def read_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
    return md_content

def read_tables(md_content):
    soup = BeautifulSoup(md_content, 'html.parser')
    tables = soup.find_all('table')
    table_datas = []  # 存储所有表格的数据

    # 遍历文档中的每个表格
    for table in tables:
        table_data = []  # 存储单个表格的数据

        # 处理表头，查找 thead 中的 th 和 td 标签
        thead = table.find('thead')
        if thead:
            headers = []
            for element in thead.find_all(['th', 'td']):
                img = element.find('img')
                if img:
                    # 调用 reorder_img_attributes 函数重组 img 标签
                    cell_content = reorder_img_attributes(img)  # 处理 <img> 标签
                else:
                    cell_content = element.get_text(strip=True)  # 只提取纯文本

                # 创建单元格信息字典
                cell_info = {'content': cell_content}

                # 添加 rowspan、colspan 和 style 属性
                rowspan = element.get('rowspan')
                colspan = element.get('colspan')
                style = element.get('style')
                if rowspan:
                    cell_info['rowspan'] = rowspan
                if colspan:
                    cell_info['colspan'] = colspan
                if style:
                    cell_info['style'] = style

                headers.append(cell_info)
            table_data.append(headers)  # 将表头添加到 table_data

        # 处理表体，查找 tbody 中的所有行和列
        tbody = table.find('tbody')
        if tbody:
            body_rows = []
            for row in tbody.find_all('tr'):
                cols = []
                for col in row.find_all('td'):
                    img = col.find('img')
                    if img:
                        # 调用 reorder_img_attributes 函数重组 img 标签
                        cell_content = reorder_img_attributes(img)  # 处理 <img> 标签
                    else:
                        cell_content = col.get_text(strip=True)  # 只提取纯文本

                    # 创建单元格信息字典
                    cell_info = {'content': cell_content}

                    # 添加 rowspan、colspan 和 style 属性
                    rowspan = col.get('rowspan')
                    colspan = col.get('colspan')
                    style = col.get('style')
                    if rowspan:
                        cell_info['rowspan'] = rowspan
                    if colspan:
                        cell_info['colspan'] = colspan
                    if style:
                        cell_info['style'] = style

                    cols.append(cell_info)
                body_rows.append(cols)
            table_data.extend(body_rows)  # 将表体数据添加到 table_data

        table_datas.append(table_data)  # 将整个表格的数据添加到 table_datas

    return table_datas


def process_table_header(headers, indent):
    """处理表头部分，返回带缩进的 HTML 字符串。"""
    header_html = f'{indent * 1}<thead>\n'
    header_html += f'{indent * 2}<tr>\n'

    for header in headers:
        # 提取内容
        content = header.get('content', '')
        # 保留 colspan 属性
        colspan = f' colspan="{header["colspan"]}"' if 'colspan' in header else ''

        # 设置左对齐，清空其他属性
        style = ' style="text-align: left;"'

        # 构建 <th> 标签，只保留左对齐的样式和 colspan
        header_html += f'{indent * 3}<th{colspan}{style}>{content}</th>\n'

    header_html += f'{indent * 2}</tr>\n'
    header_html += f'{indent * 1}</thead>\n'
    return header_html


def process_table_body(rows, indent, has_thead=False):
    """处理表体部分，返回带缩进的 HTML 字符串。"""
    body_html = f'{indent * 1}<tbody>\n'
    td_count = 0
    widths = []

    for i, row in enumerate(rows):
        body_html += f'{indent * 2}<tr>\n'

        # 只为第一个 <tr> 中的 <td> 或 <th> 设置属性
        if i == 0:
            td_count = len(row)
            if td_count == 2:
                widths = ['20%', '80%']
            elif td_count == 3:
                widths = ['35%', '30%', '35%']
            else:
                widths = [''] * td_count  # 如果 <td> 数量不是 2 或 3，不设置宽度

            # 遍历第一个 <tr> 中的所有 <td> 或 <th>
            for j, col in enumerate(row):
                # 提取内容和属性
                content = col.get('content', '')
                rowspan = f' rowspan="{col["rowspan"]}"' if 'rowspan' in col else ''
                colspan = f' colspan="{col["colspan"]}"' if 'colspan' in col else ''
                # 构建 style 字符串，将宽度放在第一个
                width_style = f'width: {widths[j]}; ' if widths[j] else ''

                # 默认设置左对齐
                if '<img' in content:
                    # 如果包含 <img>，为图片设置居中
                    style = f' style="{width_style}text-align: center;"'
                    # 使用 <td>，无论是否存在 <thead>
                    body_html += f'{indent * 3}<td{style}{rowspan}{colspan}>{content}</td>\n'
                else:
                    # 不包含 <img>，根据是否有 <thead> 决定标签类型
                    style = f' style="{width_style}text-align: left;"'
                    # 如果有 <thead>，第一个 <tr> 的子项都设为 <td>
                    tag = 'td'
                    body_html += f'{indent * 3}<{tag}{style}{rowspan}{colspan}>{content}</{tag}>\n'
        else:
            # 对于其他 <tr>，不设置任何属性
            for j, col in enumerate(row):
                # 仅提取内容
                content = col.get('content', '')

                # 判断是否包含 <img>
                if '<img' in content:
                    # 包含 <img>，直接添加内容，不设置任何属性
                    content = f'<div style="text-align: center;">{content}</div>'
                    body_html += f'{indent * 3}<td>{content}</td>\n'
                else:
                    # 不包含 <img>，直接处理为正常的 <td>，不设置任何属性
                    body_html += f'{indent * 3}<td>{content}</td>\n'

        body_html += f'{indent * 2}</tr>\n'
    body_html += f'{indent * 1}</tbody>\n'
    return body_html


def create_new_table(table_data, indent="  "):
    html_table = '<table>\n'

    # 判断第一个列表是否包含图片
    first_row_contains_img = any(
        isinstance(item, dict) and ('content' in item) and ('.jpg' in item['content'] or '.png' in item['content'] or '.jpeg' in item['content'])
        for item in table_data[0]
    )

    if not first_row_contains_img:
        # 如果第一个列表不含图片，作为表头 <thead>
        headers_html = process_table_header(table_data[0], indent)
        html_table += headers_html

        # 剩下的部分作为表体 <tbody>
        body_html = process_table_body(table_data[1:], indent, has_thead=True)
        html_table += body_html
    else:
        # 如果第一个列表含有图片，将所有内容作为 <tbody>
        body_html = process_table_body(table_data, indent, has_thead=False)
        html_table += body_html

    html_table += '</table>'
    return html_table


def format_all_table(file_path):
    #file_path = r'F:\Desktop\ed-docs\docs\zh\hmi3020-070c\ds\README.md'  # 原始 Markdown 文件路径

    # 读取 Markdown 文件内容
    md_content = read_markdown(file_path)
    soup = BeautifulSoup(md_content, 'html.parser')
    # 提取表格数据
    table_datas = read_tables(md_content)

    formatted_html = str(soup)

    # 对文档中的每个表格重新生成格式化后的表格并添加缩进
    for table, table_data in zip(soup.find_all('table'), table_datas):
        # 生成新的表格 HTML
        formatted_table = create_new_table(table_data)
        formatted_html = formatted_html.replace(str(table), formatted_table)

    # 将修改后的内容写回新的 Markdown 文件
    write_file(file_path, formatted_html)
