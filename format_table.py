from bs4 import BeautifulSoup
import os


def reorder_img_attributes(img):
    """重新排序img标签的属性，使src放在alt前面"""
    # 获取所有属性
    attrs = img.attrs
    # 将属性重组为 src 在 alt 之前
    src = attrs.get('src', '')
    alt = attrs.get('alt', '')

    # 重建 <img> 标签
    new_img_tag = f'<img src="{src}" alt="{alt}"'

    # 保留其他属性（如 style），并将其添加到新标签中
    for attr, value in attrs.items():
        if attr not in ['src', 'alt']:
            new_img_tag += f' {attr}="{value}"'

    # 闭合标签
    new_img_tag += '>'

    return new_img_tag

# 提取表格内容
def extract_table_data(table):
    table_data = []

    # 处理表头，查找 thead 中的 th 和 td 标签
    thead = table.find('thead')
    if thead:
        headers = []
        for element in thead.find_all(['th', 'td']):
            img = element.find('img')
            if img:
                # 调用 reorder_img_attributes 函数重组 img 标签
                headers.append(reorder_img_attributes(img))
            else:
                headers.append(element.get_text(strip=True))  # 只提取纯文本
        table_data.append(headers)

    # 处理表体，查找 tbody 中的所有行和列
    tbody = table.find('tbody')
    if tbody:
        for row in tbody.find_all('tr'):
            cols = []
            for col in row.find_all('td'):
                img = col.find('img')
                if img:
                    # 调用 reorder_img_attributes 函数重组 img 标签
                    cols.append(reorder_img_attributes(img))
                else:
                    cols.append(col.get_text(strip=True))  # 只提取纯文本
            table_data.append(cols)

    return table_data



# 创建新的 HTML 表格
# 创建新的 HTML 表格
# 创建新的 HTML 表格（不处理 style 和缩进）
def create_new_table(table_data):
    html_table = '<table>\n'

    # 判断第一个列表是否包含图片
    first_row_contains_img = any(
        '.jpg' in item or '.png' in item or '.jpeg' in item for item in table_data[0])

    if not first_row_contains_img:
        # 如果第一个列表不含图片，作为表头 <thead>
        html_table += '  <thead>\n    <tr>\n'
        for header in table_data[0]:
            html_table += f'      <th>{header}</th>\n'
        html_table += '    </tr>\n  </thead>\n'

        # 剩下的部分作为表体 <tbody>
        html_table += '  <tbody>\n'
        for row in table_data[1:]:
            html_table += '    <tr>\n'
            for col in row:
                html_table += f'      <td>{col}</td>\n'
            html_table += '    </tr>\n'
        html_table += '  </tbody>\n'
    else:
        # 如果第一个列表含有图片，将所有内容作为 <tbody>
        html_table += '  <tbody>\n'
        for row in table_data:
            html_table += '    <tr>\n'
            for col in row:
                html_table += f'      <td>{col}</td>\n'
            html_table += '    </tr>\n'
        html_table += '  </tbody>\n'

    html_table += '</table>'
    return html_table



# 为表格元素添加缩进的函数
# 为表格元素添加缩进的函数
def add_indent_to_table(table_soup, indent="  "):
    """
    为 BeautifulSoup 对象中的表格元素添加缩进，并设置 <th> 左对齐，<td> 宽度。如果 <thead> 中第一个 <tr> 只有一个 <th>，则为其添加 colspan="2"。

    :param table_soup: BeautifulSoup 表格对象
    :param indent: 缩进字符串，默认两个空格
    """
    formatted_html = ""

    # 添加表格标签
    formatted_html += '<table>\n'

    # 处理表头
    thead = table_soup.find('thead')
    if thead:
        formatted_html += f'{indent * 1}<thead>\n'
        for row in thead.find_all('tr'):
            formatted_html += f'{indent * 2}<tr>\n'
            th_elements = row.find_all('th')
            # 如果 <tr> 中只有一个 <th>，添加 colspan="2"
            if len(th_elements) == 1:
                formatted_html += f'{indent * 3}<th colspan="2" style="text-align: left;">{th_elements[0].get_text(strip=True)}</th>\n'
            else:
                for th in th_elements:
                    formatted_html += f'{indent * 3}<th style="text-align: left;">{th.get_text(strip=True)}</th>\n'
            formatted_html += f'{indent * 2}</tr>\n'
        formatted_html += f'{indent * 1}</thead>\n'

    # 处理表体
    tbody = table_soup.find('tbody')
    if tbody:
        formatted_html += f'{indent * 1}<tbody>\n'
        td_count = 0
        widths = []
        for i, row in enumerate(tbody.find_all('tr')):
            formatted_html += f'{indent * 2}<tr>\n'
            # 在第一个 tr 中为 td 设置宽度
            if i == 0:
                td_count = len(row.find_all('td'))
                if td_count == 2:
                    widths = ['20%', '80%']
                elif td_count == 3:
                    widths = ['35%', '30%', '35%']
                else:
                    widths = [''] * td_count  # 如果td数量不是2或3，不设置宽度
            for j, td in enumerate(row.find_all('td')):
                if i == 0 and td_count in [2, 3]:
                    # 为第一个 <tr> 的 <td> 设置宽度，格式为 style="width: xx%;"
                    formatted_html += f'{indent * 3}<td style="width: {widths[j]};">{td.get_text(strip=True)}</td>\n'
                else:
                    formatted_html += f'{indent * 3}<td>{td.get_text(strip=True)}</td>\n'
            formatted_html += f'{indent * 2}</tr>\n'
        formatted_html += f'{indent * 1}</tbody>\n'

    formatted_html += f'{indent}</table>\n'

    return formatted_html


def format_all_table(file_path):
    # 读取 Markdown 文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()

    # 使用 BeautifulSoup 解析 HTML 表格
    soup = BeautifulSoup(md_content, 'html.parser')

    # 找到 Markdown 文档中的所有 HTML 表格
    tables = soup.find_all('table')

    # 打印文档中找到的表格数量
    print(f"文档中找到的表格数量: {len(tables)}")

    # 用于存储新表格的列表
    html_table_list = []

    # 处理每个原始表格，生成新的表格
    for table in tables:
        table_data = extract_table_data(table)  # 提取表格数据
        new_table_html = create_new_table(table_data)  # 创建新表格
        html_table_list.append(new_table_html)  # 将新表格存入列表

    # 确保文档中的表格数量和新生成的表格数量一致
    if len(tables) != len(html_table_list):
        raise ValueError("文档中的表格数量和生成的新表格数量不一致。")

    # 使用 BeautifulSoup 直接替换表格
    for original_table, new_table_html in zip(tables, html_table_list):
        # 使用新的 HTML 表格替换原始表格
        new_table_soup = BeautifulSoup(new_table_html, 'html.parser')
        original_table.replace_with(new_table_soup)

    # 为表格添加缩进并保留非表格内容
    formatted_html = str(soup)

    # 对文档中的每个表格重新生成格式化后的表格并添加缩进
    for table in soup.find_all('table'):
        formatted_table = add_indent_to_table(table)
        formatted_html = formatted_html.replace(str(table), formatted_table)

    # 将修改后的文档直接写回原文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(formatted_html)

    print(f"表格已修改并保存至原文件: {file_path}")

# 使用示例
# file_path = r'F:\Desktop\temp\zh\hmi2120-070c\um\1-hardware\README.md'  # 修改为你的文件路径
# format_all_table(file_path)
