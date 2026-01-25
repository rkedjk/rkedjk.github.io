import re

def convert_md_to_js(input_filename, output_filename):
    # Читаем исходный файл
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Файл {input_filename} не найден.")
        return

    # Регулярное выражение для поиска заголовков
    # Ищет строки вида: # **1\. Название темы**
    header_pattern = re.compile(r'^# \*\*(?P<number>\d+)\\\.\s+(?P<title>.*?)\*\*', re.MULTILINE)

    matches = list(header_pattern.finditer(text))
    tickets = []

    for i, match in enumerate(matches):
        number = match.group('number')
        raw_title = match.group('title').strip()
        # Формируем заголовок как в примере: "1. Название"
        title = f"{number}. {raw_title}"

        # Определяем границы контента: от конца текущего заголовка до начала следующего
        start_pos = match.end()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        
        # Извлекаем и чистим контент
        content = text[start_pos:end_pos].strip()
        
        # Экранируем обратные кавычки, чтобы не сломать JS шаблонную строку
        content = content.replace('`', '\\`')

        tickets.append({
            'number': number,
            'title': title,
            'content': content
        })

    # Формируем итоговый JS файл
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("const tickets = [\n")
        
        for ticket in tickets:
            f.write("                {\n")
            f.write(f"                    number: {ticket['number']},\n")
            f.write(f"                    title: \"{ticket['title']}\",\n")
            f.write(f"                    content: `\n{ticket['content']}\n`\n")
            f.write("                },\n")
            
        f.write("];")
    
    print(f"Готово! Обработано билетов: {len(tickets)}. Результат сохранен в {output_filename}")

# Запуск функции
# Убедитесь, что имя файла совпадает с вашим (Untitled-document.md)
convert_md_to_js('Untitled-document.md', 'tickets.js')
