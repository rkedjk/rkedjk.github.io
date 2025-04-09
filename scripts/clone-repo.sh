#!/bin/bash
# Клонирование репозитория через GitHub CLI

if ! command -v gh &> /dev/null; then
    echo "GitHub CLI не установлен. Сначала выполните скрипт установки."
    exit 1
fi

св
echo "Клонирование репозитория super/main..."
gh repo clone super main

echo "Готово! Репозиторий склонирован в папку super"

echo "Запуск скрипта обновления/установки"

cd ~/super/main

chmod +x install.sh

./install.sh