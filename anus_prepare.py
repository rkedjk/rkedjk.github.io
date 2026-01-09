#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для преобразования Markdown-файла с билетами в JavaScript массив
для HTML-страницы шпаргалок.
"""

import re
import json
import sys


def parse_markdown_to_tickets(md_content):
    """
    Парсит Markdown-файл и преобразует в массив билетов.

    Args:
        md_content: строка с содержимым MD-файла

    Returns:
        list: массив словарей с билетами
    """
    tickets = []

    # Разделяем по заголовкам первого уровня (# N. Название)
    pattern = r'^# (\d+)\.\s+(.+?)$'

    # Находим все позиции заголовков
    matches = list(re.finditer(pattern, md_content, re.MULTILINE))

    for i, match in enumerate(matches):
        number = int(match.group(1))
        title = match.group(2).strip()

        # Определяем начало и конец содержимого билета
        content_start = match.end()
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(md_content)

        # Извлекаем содержимое билета
        content = md_content[content_start:content_end].strip()

        # Удаляем лишние пустые строки в начале и конце
        content = '\n'.join(line for line in content.split('\n'))

        tickets.append({
            'number': number,
            'title': title,
            'content': content
        })

    return tickets


def generate_javascript_array(tickets):
    """
    Генерирует JavaScript код массива tickets.

    Args:
        tickets: список словарей с билетами

    Returns:
        str: JavaScript код
    """
    js_code = "const tickets = [\n"

    for ticket in tickets:
        # Экранируем содержимое для JavaScript
        content_escaped = ticket['content'].replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

        js_code += f"""    {{
        number: {ticket['number']},
        title: "{ticket['title']}",
        content: `
{content_escaped}
`
    }},
"""

    js_code += "];"
    return js_code


def main():
    if len(sys.argv) < 2:
        print("Использование: python md_to_tickets.py <input.md> [output.js]")
        print("Если output.js не указан, результат выводится в консоль")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        # Читаем MD-файл
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Парсим билеты
        tickets = parse_markdown_to_tickets(md_content)

        if not tickets:
            print("Ошибка: Не найдено ни одного билета в файле!")
            print("Убедитесь, что билеты начинаются с '# N. Название'")
            sys.exit(1)

        print(f"Найдено билетов: {len(tickets)}")

        # Генерируем JavaScript
        js_code = generate_javascript_array(tickets)

        # Выводим или сохраняем результат
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(js_code)
            print(f"Результат сохранен в: {output_file}")
        else:
            print("\n" + "="*60)
            print("Скопируйте код ниже в HTML-файл:")
            print("="*60 + "\n")
            print(js_code)

    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден!")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
