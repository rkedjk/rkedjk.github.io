import subprocess
import re

def convert_markdown_to_html(markdown_text):
    # Пишем markdown текст во временный файл
    with open('temp.md', 'w', encoding='utf-8') as temp_markdown_file:
        temp_markdown_file.write(markdown_text)
    
    # Используем Pandoc для конвертации markdown в HTML
    result = subprocess.run(['pandoc', 'temp.md', '-f', 'markdown', '-t', 'html'], capture_output=True, text=True)
    
    # Удаляем временный файл
    subprocess.run(['rm', 'temp.md'])
    
    if result.returncode != 0:
        raise Exception(f'Pandoc conversion failed: {result.stderr}')
    
    return result.stdout

def clean_html(html_text):
    # Регулярное выражение для удаления ненужных тегов <ol type="1"> и <ol start="X" type="1">
    html_text = re.sub(r'<ol\s+(start="\d+"\s+)?type="1">', '<ol>', html_text)
    return html_text

def create_accordion_html(html_text):
    # Регулярные выражения для разделения текста на секции по заголовкам h1
    header_regex = re.compile(r'(<h1[^>]*>.*?</h1>)', re.DOTALL)
    
    # Разделяем текст по заголовкам h1
    sections = header_regex.split(html_text)
    
    html_output = []
    
    # Индексирование заголовков h1
    h1_count = 0
    
    for i in range(len(sections)):
        if header_regex.match(sections[i]):
            h1_count += 1
            header = sections[i]
            content = sections[i + 1] if i + 1 < len(sections) else ''
            
            # Создаем HTML для аккордеона
            accordion_html = f'''
            <div class="accordion">
                <div class="accordion-header" onclick="toggleAccordion(this)">
                    <span>{re.sub(r'<[^>]+>', '', header)}</span>
                    <button class="hide-button" onclick="showOverlay(event)"></button>
                </div>
                <div class="accordion-content" data-original-content="{content}">
                    {header}
                    <div>{content}</div>
                </div>
            </div>
            '''
            html_output.append(accordion_html)
    
    return '\n'.join(html_output)

def read_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def write_html_file(filepath, html_content):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(html_content)

# Пример использования
markdown_filepath = 'input.md'
html_filepath = 'output.html'

markdown_text = read_markdown_file(markdown_filepath)
html_content = convert_markdown_to_html(markdown_text)
clean_html_content = clean_html(html_content)
accordion_html_content = create_accordion_html(clean_html_content)
write_html_file(html_filepath, accordion_html_content)
