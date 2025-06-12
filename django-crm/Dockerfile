FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 安裝系統必要套件
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Python 套件
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 複製程式碼
COPY . /app/


ENV DEBUG=True
ENV SECRET_KEY=abc123