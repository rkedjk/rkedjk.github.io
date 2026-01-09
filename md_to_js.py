#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для преобразования Markdown-файла в JavaScript массив
для HTML-страницы шпаргалок.
Поддерживает форматы:
- # N. Название
- # ЗадачаN. Текст
- # Название
"""

import re
import sys


def extract_number_and_title(header_text):
    """
    Извлекает номер и название из заголовка.

    Args:
        header_text: текст заголовка без символа #

    Returns:
        tuple: (number, title)
    """
    # Убираем начальные/конечные пробелы
    text = header_text.strip()

    # Паттерн 1: "N. Название" (число в начале с точкой)
    match = re.match(r'^(\d+)\.\s*(.+)$', text)
    if match:
        return int(match.group(1)), match.group(2).strip()

    # Паттерн 2: "ЗадачаN\. " или "ЗадачаN. " или "БилетN. "
    match = re.match(r'^([А-Яа-яA-Za-z]+)(\d+)\\.?\s*(.*)$', text)
    if match:
        prefix = match.group(1)
        number = int(match.group(2))
        title_part = match.group(3).strip()
        # Если после номера есть текст, используем его как заголовок
        if title_part:
            title = title_part
        else:
            title = f"{prefix} {number}"
        return number, title

    # Паттерн 3: просто число в начале (без точки)
    match = re.match(r'^(\d+)\s+(.+)$', text)
    if match:
        return int(match.group(1)), match.group(2).strip()

    # Паттерн 4: число где-то внутри текста
    match = re.search(r'(\d+)', text)
    if match:
        return int(match.group(1)), text

    # Если номер не найден, возвращаем None и весь текст как заголовок
    return None, text


def parse_markdown_to_items(md_content):
    """
    Парсит Markdown-файл и преобразует в массив элементов.

    Args:
        md_content: строка с содержимым MD-файла

    Returns:
        list: массив словарей с элементами
    """
    items = []

    # Находим все заголовки первого уровня
    pattern = r'^#\s+(.+?)$'
    matches = list(re.finditer(pattern, md_content, re.MULTILINE))

    if not matches:
        return []

    for i, match in enumerate(matches):
        header_text = match.group(1)
        number, title = extract_number_and_title(header_text)

        # Если номер не найден, используем порядковый номер
        if number is None:
            number = i + 1

        # Определяем начало и конец содержимого
        content_start = match.end()
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(md_content)

        # Извлекаем содержимое
        content = md_content[content_start:content_end].strip()

        items.append({
            'number': number,
            'title': title,
            'content': content
        })

    return items


def generate_javascript_array(items, array_name='items'):
    """
    Генерирует JavaScript код массива.

    Args:
        items: список словарей с элементами
        array_name: имя массива в JavaScript

    Returns:
        str: JavaScript код
    """
    js_code = f"const {array_name} = [\n"

    for item in items:
        # Экранируем содержимое для JavaScript
        content_escaped = (item['content']
                          .replace('\\', '\\\\')
                          .replace('`', '\\`')
                          .replace('${', '\\${'))

        # Экранируем заголовок для JavaScript строки
        title_escaped = item['title'].replace('"', '\\"').replace('\\', '\\\\')

        js_code += f"""    {{
        number: {item['number']},
        title: "{title_escaped}",
        content: `
{content_escaped}
`
    }},
"""

    js_code += "];"
    return js_code


def main():
    if len(sys.argv) < 2:
        print("Использование: python md_to_js.py <input.md> [output.js] [array_name]")
        print()
        print("Аргументы:")
        print("  input.md    - входной Markdown файл")
        print("  output.js   - выходной JavaScript файл (опционально)")
        print("  array_name  - имя массива (по умолчанию: items)")
        print()
        print("Примеры:")
        print("  python md_to_js.py tickets.md")
        print("  python md_to_js.py tasks.md tasks.js tasks")
        print()
        print("Поддерживаемые форматы заголовков:")
        print("  # 1. Название")
        print("  # Задача15\\. Текст")
        print("  # БилетN. Название")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    array_name = sys.argv[3] if len(sys.argv) > 3 else 'items'

    try:
        # Читаем MD-файл
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Парсим элементы
        items = parse_markdown_to_items(md_content)

        if not items:
            print("Ошибка: Не найдено ни одного заголовка первого уровня (#)!")
            print("Убедитесь, что в файле есть заголовки формата: # Название")
            sys.exit(1)

        print(f"✅ Найдено элементов: {len(items)}")

        # Показываем распознанные элементы
        print("\nРаспознанные элементы:")
        for item in items[:5]:  # Показываем первые 5
            print(f"  #{item['number']} - {item['title'][:50]}...")
        if len(items) > 5:
            print(f"  ... и еще {len(items) - 5}")

        # Генерируем JavaScript
        js_code = generate_javascript_array(items, array_name)

        # Выводим или сохраняем результат
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(js_code)
            print(f"\n✅ Результат сохранен в: {output_file}")
        else:
            print("\n" + "="*70)
            print(f"Скопируйте код ниже и замените 'const {array_name} = [];' в HTML:")
            print("="*70 + "\n")
            print(js_code)

    except FileNotFoundError:
        print(f"❌ Ошибка: Файл '{input_file}' не найден!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
