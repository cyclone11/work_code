from bs4 import BeautifulSoup
import os
import re


def write_file(file_path, content):
    """
    将指定的内容写入到文件中。
    参数: file_path (str): 文件的路径，包含文件名和扩展名。
         content (str): 需要写入文件的内容。
    返回: None: 该函数没有返回值。
    异常处理: 如果文件路径不存在或文件不可写，函数会抛出 IOError 或 FileNotFoundError 异常。
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def reorder_img_attributes(img):
    """
    重新排序 img 标签的属性，使 src 放在 alt 之前，并将 alt 设置为 src 的文件名。
    参数: img (Tag): BeautifulSoup 解析出的 img 标签。
    返回: str: 重新格式化后的 img 标签字符串，src 在前，alt 设为 src 的文件名。
    备注: 该函数假设 img 标签存在 src 属性。如果不存在，返回的 img 标签中 src 将为空。
    """
    attrs = img.attrs
    src = attrs.get('src', '')
    new_img_tag = f'<img src="{src}" alt="{os.path.basename(src)}">'
    return new_img_tag

def read_markdown(file_path):
    """
    读取指定路径的 Markdown 文件，并返回文件的内容作为字符串。
    参数: file_path (str): 文件的路径，包含文件名和扩展名。
    返回: str: Markdown 文件的全部内容，包含换行符等字符。如果文件内容为空，则返回空字符串。
    异常处理: 如果文件路径不存在或文件不可读，函数会抛出 IOError 或 FileNotFoundError 异常。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def read_tables(md_content):
    """
    从 Markdown 或 HTML 内容中提取表格数据。
    参数: md_content (str): 包含表格的 Markdown 或 HTML 字符串内容。
    返回: list: 一个包含表格数据的列表，每个表格的数据包含表头和表体的内容。
    """
    # 使用 BeautifulSoup 解析传入的内容
    soup = BeautifulSoup(md_content, 'html.parser')

    # 查找所有表格
    tables = soup.find_all('table')

    # 用于存储所有提取的表格数据
    table_datas = []

    # 遍历每个表格，提取其内容
    for table in tables:
        # 用于存储单个表格的数据
        table_data = []

        # 处理表头部分
        thead = table.find('thead')  # 查找表头 thead 标签
        if thead:
            headers = []  # 用于存储表头数据的列表
            for element in thead.find_all(['th', 'td']):  # 查找表头中的所有 th 和 td
                # 检查是否存在 img 标签，并处理它
                img = element.find('img')
                cell_content = reorder_img_attributes(img) if img else element.get_text(strip=True)

                # 创建单元格信息字典，保存单元格内容
                cell_info = {'content': cell_content}

                # 如果存在 rowspan 或 colspan 属性，添加到字典中
                if element.get('rowspan'):
                    cell_info['rowspan'] = element.get('rowspan')
                if element.get('colspan'):
                    cell_info['colspan'] = element.get('colspan')

                # 将该单元格信息添加到 headers 列表中
                headers.append(cell_info)
            # 将 headers 列表添加到表格数据中
            table_data.append(headers)

        # 处理表体部分
        tbody = table.find('tbody')  # 查找表体 tbody 标签
        if tbody:
            body_rows = []  # 用于存储表体中所有行的数据
            for row in tbody.find_all('tr'):  # 遍历表体中的每一行
                cols = []  # 用于存储一行中的所有列数据
                for col in row.find_all('td'):  # 遍历每一行中的所有单元格 (td)
                    # 检查是否存在 img 标签，并处理它
                    img = col.find('img')
                    cell_content = reorder_img_attributes(img) if img else col.get_text(strip=True)

                    # 创建单元格信息字典，保存单元格内容
                    cell_info = {'content': cell_content}

                    # 如果存在 rowspan 或 colspan 属性，添加到字典中
                    if col.get('rowspan'):
                        cell_info['rowspan'] = col.get('rowspan')
                    if col.get('colspan'):
                        cell_info['colspan'] = col.get('colspan')

                    # 将该单元格信息添加到 cols 列表中
                    cols.append(cell_info)

                # 将该行的列数据添加到 body_rows 列表中
                body_rows.append(cols)

            # 将表体数据添加到表格数据中
            table_data.extend(body_rows)

        # 将表格的数据添加到最终的表格数据列表中
        table_datas.append(table_data)

    # 返回提取的所有表格数据
    # print(table_datas)
    return table_datas


def process_table_header(headers, indent):
    """处理表头部分，返回带缩进的 HTML 字符串。"""
    header_html = f'{indent * 1}<thead>\n'
    header_html += f'{indent * 2}<tr>\n'

    for header in headers:
        content = header.get('content', '')
        colspan = f' colspan="{header["colspan"]}"' if 'colspan' in header and header['colspan'] else ''
        rowspan = f' rowspan="{header["rowspan"]}"' if 'rowspan' in header and header['rowspan'] else ''
        style = ' style="text-align: left;"'
        header_html += f'{indent * 3}<th{colspan}{rowspan}{style}>{content}</th>\n'

    header_html += f'{indent * 2}</tr>\n'
    header_html += f'{indent * 1}</thead>\n'
    return header_html

def process_table_body(rows, indent, has_thead):
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
                content = col.get('content', '')
                rowspan = f' rowspan="{col["rowspan"]}"' if 'rowspan' in col else ''
                colspan = f' colspan="{col["colspan"]}"' if 'colspan' in col else ''
                # 构建 style 字符串，将宽度放在第一个
                width_style = f'width: {widths[j]}; ' if widths[j] else ''

                if has_thead:
                    # 如果有表头，只设置宽度，不设置对齐方式
                    style = f' style="{width_style}"'
                    body_html += f'{indent * 3}<td{style}{rowspan}{colspan}>{content}</td>\n'
                else:
                    # 如果没有表头，设置宽度和左对齐，并将不含图片的 <td> 转为 <th>
                    if '<img' in content:
                        style = f' style="{width_style}text-align: center;"'
                        body_html += f'{indent * 3}<td{style}{rowspan}{colspan}>{content}</td>\n'
                    else:
                        style = f' style="{width_style}text-align: left;"'
                        body_html += f'{indent * 3}<th{style}{rowspan}{colspan}>{content}</th>\n'
        else:
            # 对于其他 <tr>，不设置任何属性，但保留 colspan 和 rowspan
            for j, col in enumerate(row):
                content = col.get('content', '')
                rowspan = f' rowspan="{col["rowspan"]}"' if 'rowspan' in col else ''
                colspan = f' colspan="{col["colspan"]}"' if 'colspan' in col else ''
                body_html += f'{indent * 3}<td{rowspan}{colspan}>{content}</td>\n'

        body_html += f'{indent * 2}</tr>\n'
    body_html += f'{indent * 1}</tbody>\n'
    return body_html


def create_new_table(table_data, indent="  "):
    # 检查 tableData 是否为空
    if not table_data or len(table_data) == 0:
        print('###############')
        print("Error: table_data is empty!")
        print('###############')
        return ''

    html_table = '<table>\n'

    # 判断第一个列表是否包含图片
    first_row_contains_img = any(
        isinstance(item, dict) and ('content' in item) and any(ext in item['content'].lower() for ext in ['.jpg', '.png', '.jpeg'])
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
    """格式化所有表格"""
    md_content = read_markdown(file_path)
    soup = BeautifulSoup(md_content, 'html.parser')
    table_datas = read_tables(md_content)

    formatted_html = str(soup)

    if len(soup.find_all('table')) != len(table_datas):
        print("Error: Mismatch between tables in document and extracted table data")
        return

    for table, table_data in zip(soup.find_all('table'), table_datas):
        formatted_table = create_new_table(table_data)
        formatted_html = formatted_html.replace(str(table), formatted_table)

    write_file(file_path, formatted_html)
