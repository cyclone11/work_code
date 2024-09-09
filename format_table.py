from bs4 import BeautifulSoup

# 要删除的标签列表，用户可以自行添加
TAGS_TO_REMOVE = ['p', 'span', 'strong']


# 删除表格中的特定属性（不处理 img 标签）
def remove_attributes(element):
    if element.name != 'img':  # 忽略 img 标签，保持 img 的属性不被修改
        if 'class' in element.attrs:
            del element.attrs['class']
        if 'style' in element.attrs:
            del element.attrs['style']
        if 'border' in element.attrs:
            del element.attrs['border']

    # 递归遍历所有子元素
    for child in element.find_all(True):
        if child.name != 'img':  # 确保递归时也跳过 img 标签
            remove_attributes(child)


# 删除指定的标签，保留其内容
def remove_tags(soup, tags_to_remove):
    for tag in tags_to_remove:
        for element in soup.find_all(tag):
            element.unwrap()  # unwrap 保留内容但删除标签


# 将 thead 中的所有 tr 的 td 变为 th，并将 th 或 td 设置左对齐
def convert_thead_td_to_th(table, soup):
    thead = table.find('thead')
    tbody = table.find('tbody')
    if thead and tbody:
        first_tr_tbody = tbody.find('tr')
        if first_tr_tbody:
            tbody_td_count = len(first_tr_tbody.find_all('td'))
            for tr in thead.find_all('tr'):
                ths = tr.find_all(['td', 'th'])
                if len(ths) == 1:
                    ths[0]['colspan'] = str(tbody_td_count)
                for td in ths:
                    if td.name == 'td':
                        th = soup.new_tag('th')
                        th.string = td.string
                        th['style'] = 'text-align: left'
                        td.replace_with(th)
                    else:
                        td['style'] = 'text-align: left'


# 设置 tbody 第一个 tr 的 td 宽度
def set_tbody_first_tr_width(table):
    tbody = table.find('tbody')
    if tbody:
        first_tr = tbody.find('tr')
        if first_tr:
            tds = first_tr.find_all('td')
            if len(tds) == 2:
                tds[0]['style'] = 'width: 20%'
                tds[1]['style'] = 'width: 80%'
            elif len(tds) == 3:
                tds[0]['style'] = 'width: 40%'
                tds[1]['style'] = 'width: 30%'
                tds[2]['style'] = 'width: 30%'


# 如果没有 thead，将 tbody 第一个 tr 设置为 thead
def promote_first_tr_to_thead(table, soup):
    thead = table.find('thead')
    tbody = table.find('tbody')
    if not thead and tbody:
        first_tr = tbody.find('tr')
        if first_tr and not first_tr.find('img'):
            new_thead = soup.new_tag('thead')
            new_thead.append(first_tr)
            table.insert(0, new_thead)


# 处理表格
def process_table(table, soup):
    promote_first_tr_to_thead(table, soup)
    convert_thead_td_to_th(table, soup)
    set_tbody_first_tr_width(table)


# 处理文档内容
def process_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 不删除 img 标签，无论是否在表格中
    remove_attributes(soup)
    remove_tags(soup, TAGS_TO_REMOVE)

    for table in soup.find_all('table'):
        process_table(table, soup)

    return str(soup)


# 处理文件并修改原文件
def process_markdown_file_in_place(input_path):
    try:
        # 读取输入文件内容
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 处理 HTML 内容
        processed_content = process_html(content)

        # 覆盖写回原文件
        with open(input_path, 'w', encoding='utf-8') as file:
            file.write(processed_content)

        print(f"文件已处理完成第4步，并写回原文件 {input_path}")
    except Exception as e:
        print(f"处理文件时出错: {e}")

# 示例调用
# input_path = 'output.md'
# process_markdown_file_in_place(input_path)
