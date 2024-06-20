import re

# Открываем файл для чтения
with open('source3.md', 'r', encoding='utf-8') as file:
    content = file.read()

# Используем регулярное выражение для замены **<число>\. на # <число>.
updated_content = re.sub(r'\*\*(\d+)\\\.', r'# \1.', content)

# Открываем файл для записи и сохраняем измененное содержимое
with open('input.md', 'w', encoding='utf-8') as file:
    file.write(updated_content)
