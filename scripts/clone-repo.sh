#!/bin/bash
# Клонирование репозитория через GitHub CLI

if ! command -v gh &> /dev/null; then
    echo "GitHub CLI не установлен. Сначала выполните скрипт установки."
    exit 1
fi

cd ~/

mkdir super

cd ~/super

echo "Клонирование репозитория super/main..."
gh repo clone super main

echo "Готово! Репозиторий main склонирован в папку super"
echo "Очистка скриптов инициации"

sudo rm -r ~/automate

echo "Запуск скрипта обновления/установки"

cd ~/super/main

chmod u+x install.sh

./install.sh