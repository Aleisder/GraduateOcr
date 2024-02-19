# 1. Настройка проекта

## 1.1. Установка пакетов

В корне проекта находится файл `requirements.txt`, в котором указаны необходимые пакеты и их версии. Установить все пакеты из списка можно следующей командой:
```
pip install -r requirements.txt
```

## 1.2. Poppler

Для чтения, рендера и изменения PDF-файлов необходимо установить модуль `poppler`. Скачать `zip`-архив можно [здесь](https://github.com/oschwartz10612/poppler-windows/releases/).

Путь к модулю до папки `bin` нужно указать в файле `.env`:
```
POPPLER_PATH=C:\*\poppler-xx\bin
```

