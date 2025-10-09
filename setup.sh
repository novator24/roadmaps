#!/bin/bash

# Скрипт для настройки окружения проекта roadmap analysis

echo "🚀 Настройка окружения для анализа roadmap..."

# Создание виртуального окружения
echo "📦 Создание виртуального окружения..."
python3 -m venv venv

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Установка зависимостей
echo "📚 Установка зависимостей..."
pip install -r requirements.txt

echo "✅ Окружение настроено!"
echo ""
echo "Для запуска скрипта используйте:"
echo "source venv/bin/activate"
echo "python solution.py"
echo ""
echo "Для деактивации виртуального окружения:"
echo "deactivate"
