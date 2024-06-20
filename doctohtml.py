import subprocess
import re

def convert_doc_to_html(doc_filepath):
    # Команда для конвертации DOC в HTML с помощью Pandoc
    command = ['pandoc', '--wrap=none', '-f', 'doc', '-t', 'html', doc_filepath]
    result = subprocess.run(command, capture_output=True, text=True)
    html_content = result.stdout
    return html_content

def clean_html(html_content):
    # Удаление лишних тегов <ol type="1"> и <ol start="X" type="1">
    html_content = re.sub(r'<ol\s+(start="\d+"\s+)?type="1">', '<ol>', html_content)
    return html_content

def create_accordion_html(html_content):
    # Регулярные выражения для разделения текста на секции по заголовкам h1
    header_regex = re.compile(r'(<h1.*?>.*?</h1>)', re.DOTALL)
    
    # Разделяем текст по заголовкам h1
    sections = header_regex.split(html_content)
    
    html_output = []
    
    for i in range(1, len(sections), 2):
        header = re.sub(r'<.*?>', '', sections[i]).strip()
        content = sections[i + 1].strip() if i + 1 < len(sections) else ''
        
        # Создаем HTML для аккордеона
        accordion_html = f'''
        <div class="accordion">
            <div class="accordion-header" onclick="toggleAccordion(this)">
                <span>{header}</span>
                <button class="hide-button" onclick="showOverlay(event)"></button>
            </div>
            <div class="accordion-content" data-original-content="{content}">
                {sections[i]}
                <div>{content}</div>
            </div>
        </div>
        '''
        html_output.append(accordion_html)
    
    return '\n'.join(html_output)

def write_html_file(filepath, html_content):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(html_content)

# Пример использования
doc_filepath = 'input.doc'
html_filepath = 'output_z.html'

# Конвертация DOC в HTML с помощью Pandoc
html_content = convert_doc_to_html(doc_filepath)

# Очистка HTML от лишних тегов
clean_html_content = clean_html(html_content)

# Создание аккордеона
accordion_html_content = create_accordion_html(clean_html_content)

# Запись HTML файла
write_html_file(html_filepath, accordion_html_content)
