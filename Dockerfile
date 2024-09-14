FROM python:3.9-slim

# Установка зависимостей для поддержки WebP в Pillow
RUN apt-get update && \
    apt-get install -y ffmpeg libwebp-dev && \
    rm -rf /var/lib/apt/lists/*

# Установка необходимых Python-библиотек
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование скрипта в контейнер
COPY script.py /app/script.py
WORKDIR /app

# Установка команды по умолчанию
ENTRYPOINT ["python", "script.py"]