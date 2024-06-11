import re

def convert_markdown_to_html(markdown_text):
    # Regular expression to match headers and content
    header_regex = re.compile(r'^#\s*(\d+)\.\s*(.+)$', re.MULTILINE)
    subheader_regex = re.compile(r'^##\s*(.+)$', re.MULTILINE)
    subsubheader_regex = re.compile(r'^###\s*(.+)$', re.MULTILINE)
    bullet_point_regex = re.compile(r'^-\s*(.+)$', re.MULTILINE)
    number_point_regex = re.compile(r'^\d+\.\s*(.+)$', re.MULTILINE)

    html_output = []
    
    # Split into sections based on the header
    sections = re.split(header_regex, markdown_text)

    for i in range(1, len(sections), 3):
        number = sections[i]
        title = sections[i + 1]
        content = sections[i + 2]
        
        # Replace subheaders and subsubheaders
        content = subheader_regex.sub(r'<h2>\1</h2>', content)
        content = subsubheader_regex.sub(r'<h3>\1</h3>', content)

        # Replace bullet points and numbered points
        content = bullet_point_regex.sub(r'<li>\1</li>', content)
        content = number_point_regex.sub(r'<li>\1</li>', content)
        
        # Wrap bullet points and numbered points with <ul> or <ol>
        content = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', content)
        
        # Remove excess line breaks and spaces
        content = content.replace('\n', '').replace('\r', '').strip()
        
        # Create accordion HTML
        accordion_html = f'''
        <div class="accordion">
            <div class="accordion-header" onclick="toggleAccordion(this)">
                <span>{number}. {title}</span>
                <button class="hide-button" onclick="showOverlay(event)"></button>
            </div>
            <div class="accordion-content" data-original-content="{content}">
                <p>{content}</p>
            </div>
        </div>
        '''
        html_output.append(accordion_html)
    
    return '\n'.join(html_output)

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_html_file(file_path, html_content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

# Example usage
markdown_file_path = 'source.md'
html_file_path = 'output.html'

markdown_text = read_markdown_file(markdown_file_path)
html_content = convert_markdown_to_html(markdown_text)
write_html_file(html_file_path, html_content)
