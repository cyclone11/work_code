from bs4 import BeautifulSoup
import os

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
                headers.append(img['src'])  # 提取图片的 src 属性
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
                    cols.append(img['src'])  # 提取图片的 src 属性
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



# 替换 Markdown 文档中的 HTML 表格并为其添加缩进
def replace_tables_in_markdown(file_path):
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

    #print(formatted_html)
    for table in soup.find_all('table'):
        # 对每个表格重新生成格式化后的表格
        formatted_table = add_indent_to_table(table)
        formatted_html = formatted_html.replace(str(table), formatted_table)

    # 构造新文件路径，命名为 README1.md
    new_file_path = os.path.join(os.path.dirname(file_path), 'README1.md')

    # 将修改后的文档写回文件，保留原始内容并对表格添加缩进
    with open(new_file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(formatted_html)

    print(f"新表格已生成并保存至: {new_file_path}")


# 使用示例
file_path = r'F:\Desktop\ed-docs-new-style\docs\zh\ipc2400\ds\README.md'  # 你可以根据需要修改文件路径
replace_tables_in_markdown(file_path)
