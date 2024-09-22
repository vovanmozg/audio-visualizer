FROM python:3.9-slim

# Установка зависимостей для поддержки WebP в Pillow и FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg libwebp-dev libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

# Установка необходимых Python-библиотек
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование скриптов в контейнер
COPY . /app
WORKDIR /app

# Установка команды по умолчанию
ENTRYPOINT ["python", "main.py"]
