import re
from bs4 import BeautifulSoup

# 删除内容为空的标签
def delete_empty_tags(soup):
    """
    删除内容为空的标签。
    """
    for tag in soup.find_all(True):
        if not tag.text.strip():
            tag.decompose()  # 删除内容为空的标签
    return soup

# 删除表格中所有的class和style属性
def remove_class_style_and_border(soup):
    """
    删除所有标签中的 class、style 和 border 属性。
    """
    for tag in soup.find_all(True):
        for attr in ['class', 'style', 'border']:
            if attr in tag.attrs:
                del tag.attrs[attr]
    return soup

# 将thead中的th设置为左对齐
def align_thead_th(soup):
    """
    为 thead 中的 th 元素设置左对齐。
    """
    thead = soup.find('thead')
    if thead:
        for th in thead.find_all('th'):
            th['style'] = 'text-align: left'
    return soup

# 设置tbody中第一行个元素的宽度
def set_tbody_tr_widths(soup):
    """
    为 tbody 中的第一个 tr 里的 td 元素设置宽度。
    2 个 td：分别设置为 20%, 80%；
    3 个 td：分别设置为 35%, 30%, 35%。
    """
    tbody = soup.find('tbody')
    if tbody:
        first_tr = tbody.find('tr')
        if first_tr:
            tds = first_tr.find_all('td')
            if len(tds) == 2:
                tds[0]['style'] = 'width: 20%'
                tds[1]['style'] = 'width: 80%'
            elif len(tds) == 3:
                tds[0]['style'] = 'width: 35%'
                tds[1]['style'] = 'width: 30%'
                tds[2]['style'] = 'width: 35%'
    return soup

# 如果没有thead，为第一个tr中的td设置左对齐，并为img居中
def align_first_tr_if_no_thead(soup):
    """
    如果表格中没有 thead，设置第一个 tr 中的 td 为左对齐。
    如果 td 中有 img 标签，将 img 设置为居中。
    """
    tables = soup.find_all('table')
    for table in tables:
        thead = table.find('thead')
        if not thead:  # 没有 thead 时
            first_tr = table.find('tr')
            if first_tr:
                tds = first_tr.find_all('td')
                for td in tds:
                    td['style'] = 'text-align: left'  # 设置左对齐
                    img = td.find('img')
                    if img:
                        img['style'] = 'display: block; margin: 0 auto;'  # 将 img 设置为居中
    return soup

# 移除这些多余的标签
def remove_unwanted_tags(soup):
    """
    移除 <p>、<span>、<div>、<br> 标签但保留内容。
    """
    remove_tags = ['p', 'span', 'div', 'br', 'strong']
    for tag_name in remove_tags:
        for tag in soup.find_all(tag_name):
            tag.unwrap()  # 移除标签但保留内容
    return soup

# 增加缩进
def add_indent_to_html(html, indent_level=2):
    """
    为 HTML 表格添加手动缩进，并将每个 td 和 th 的开始和结束标签与其内容放在同一行。
    """
    lines = html.split('\n')
    indented_lines = []
    open_td_or_th_line = None

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith('<table') or stripped_line.startswith('</table>'):
            indented_lines.append(stripped_line)
        elif stripped_line.startswith('<thead') or stripped_line.startswith('</thead>'):
            indented_lines.append(' ' * (indent_level + 2) + stripped_line)
        elif stripped_line.startswith('<tbody') or stripped_line.startswith('</tbody>'):
            indented_lines.append(' ' * (indent_level + 2) + stripped_line)
        elif stripped_line.startswith('<tr') or stripped_line.startswith('</tr>'):
            indented_lines.append(' ' * (indent_level + 4) + stripped_line)
        elif (stripped_line.startswith('<td') or stripped_line.startswith('<th')) and (stripped_line.endswith('</td>') or stripped_line.endswith('</th>')):
            # 如果 <td> 或 <th> 标签和内容在同一行，直接加入
            indented_lines.append(' ' * (indent_level + 6) + stripped_line)
        elif stripped_line.startswith('<td') or stripped_line.startswith('<th'):
            # 如果 <td> 或 <th> 标签单独一行，暂存这一行
            open_td_or_th_line = ' ' * (indent_level + 6) + stripped_line
        elif (stripped_line.endswith('</td>') or stripped_line.endswith('</th>')) and open_td_or_th_line:
            # 将 <td> 或 <th> 标签与内容和闭合标签放在同一行
            indented_lines.append(open_td_or_th_line + ' ' + stripped_line)
            open_td_or_th_line = None
        else:
            if open_td_or_th_line:
                # 如果是 <td> 或 <th> 的内容，保持与标签在同一行
                open_td_or_th_line += ' ' + stripped_line
            else:
                indented_lines.append(line)  # 保留非 HTML 表格内容的格式

    return '\n'.join(indented_lines)

def process_html_table(input_file):
    """
    主函数：处理 HTML 表格，删除无用的属性，设置样式，删除空标签和不需要的标签。
    """
    # 读取原始文件内容
    with open(input_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 使用正则表达式删除 class, style 和 border 属性
    html_content = re.sub(r'\s*(class|style|border)="[^"]*"', '', html_content)

    # 解析 HTML 内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 删除空标签
    soup = delete_empty_tags(soup)

    # 删除 class, style 和 border 属性
    soup = remove_class_style_and_border(soup)

    # 删除 <p>、<span>、<div>、<br> 标签
    soup = remove_unwanted_tags(soup)

    # 设置 thead 中的 th 左对齐
    soup = align_thead_th(soup)

    # 设置 tbody 中第一个 tr 里的 td 宽度
    soup = set_tbody_tr_widths(soup)

    # 如果没有 thead，设置第一个 tr 的 td 左对齐，且居中 img
    soup = align_first_tr_if_no_thead(soup)

    # 将 soup 对象转换为字符串
    modified_html = str(soup)

    # 手动为 HTML 表格内容添加缩进，并将 <td> 和 <th> 标签开始和结束放在同一行
    indented_html = add_indent_to_html(modified_html)

    # 写回原始文件
    with open(input_file, 'w', encoding='utf-8') as file:
        file.write(indented_html)

    print(f"已修改 {input_file} 文件中的表格标签和属性。")

# 替换为要修改的实际文档的路径，Ctrl+Shift+F10运行代码
input_file = r'F:\Desktop\ed-docs-new-style\docs\zh\hmi2020-101c\ds\README.md'

# 程序会将文档里所有的表格设置为标准格式
process_html_table(input_file)
