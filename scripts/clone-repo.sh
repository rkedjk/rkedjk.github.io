#!/bin/bash
# Клонирование репозитория через GitHub CLI

if ! command -v gh &> /dev/null; then
    echo "GitHub CLI не установлен. Сначала выполните скрипт установки."
    exit 1
fi

read -p "Введите ваш GitHub username: " username
read -p "Введите название репозитория: " repo

echo "Клонирование репозитория $username/$repo..."
gh repo clone $username/$repo

echo "Готово! Репозиторий склонирован в папку ./$repo"