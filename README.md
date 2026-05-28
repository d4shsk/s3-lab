# Тема 9. Лабораторная работа
### Выполнил: Шарманов Даниил Андреевич

## Создание бакета

Я создал бакет и настроил его согласно инструкции.

[![image.png](https://i.postimg.cc/yYgft4Wj/image.png)](https://postimg.cc/Tpxq5sV5)

[![image.png](https://i.postimg.cc/g23gcVVy/image.png)](https://postimg.cc/9DFdJqNz)

[![image.png](https://i.postimg.cc/D0Wc9LfK/image.png)](https://postimg.cc/ctSYYK8D)

## Использование GigaCode

Я установил AWS Cli, GigaCode и написал промты как в задании. В консоли проверил их выполнение.

[![image.png](https://i.postimg.cc/c1jhQ9TG/image.png)](https://postimg.cc/vDr5yvp0)

[![image.png](https://i.postimg.cc/fR7vQwsM/image.png)](https://postimg.cc/G42Dkn9f)


## Самостоятельная работа.
#### Ролевой промт:
```text
Ты senior backend-разработчик на Python и специалист по S3 Object Storage в Yandex Cloud.

Мне нужно выполнить лабораторную работу по теме S3. Нужно реализовать веб-сервис на FastAPI для работы с Yandex Object Storage через boto3.

Требования:
1. Использовать FastAPI.
2. Использовать boto3.
3. Настройки хранить в .env:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
   - S3_BUCKET_NAME
   - S3_ENDPOINT_URL=https://storage.yandexcloud.net
4. Сервис должен уметь:
   - показывать список файлов в бакете;
   - загружать файл в бакет;
   - удалять файл из бакета;
   - генерировать presign-ссылку для просмотра файла.
5. Не использовать реальные ключи в коде.
6. Дай структуру проекта, полный код файлов и команды запуска.

Сделай решение простым и подходящим для лабораторной работы.
```

Вывод модели:

[![image.png](https://i.postimg.cc/d04mD4Ls/image.png)](https://postimg.cc/jWnJF6Hm)

Я создал файлы и установил зависимости.

#### Zero-shot промт

```text
Сгенерируй файл main.py для FastAPI-сервиса работы с Yandex Object Storage.

Требования:
- использовать FastAPI;
- реализовать GET /files для получения списка файлов;
- реализовать POST /upload для загрузки файла;
- реализовать DELETE /files/{filename} для удаления файла;
- реализовать GET /presign/{filename} для получения presign-ссылки;
- использовать функции из файла s3_client.py;
- код должен быть простым и подходящим для лабораторной работы.

Не используй реальные ключи доступа.
```

Полученный код был вставлен в файл main.py

#### One-shot промт

```python
Создай файл s3_client.py для подключения к Yandex Object Storage через boto3.

Используй этот пример подключения:

python
import boto3
import os

s3 = boto3.client(
    "s3",
    endpoint_url="https://storage.yandexcloud.net",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)
```

Результат:
```python
import boto3
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Создаём клиент S3 для Yandex Cloud
s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL", "https://storage.yandexcloud.net"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

# Имя бакета берётся из переменных окружения
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def list_files():
    """Получить список файлов в бакете"""
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    if "Contents" not in response:
        return []
    return [item["Key"] for item in response["Contents"]]


def upload_file(file_obj, filename):
    """Загрузить файл в бакет"""
    s3.upload_fileobj(file_obj, BUCKET_NAME, filename)


def delete_file(filename):
    """Удалить файл из бакета"""
    s3.delete_object(Bucket=BUCKET_NAME, Key=filename)


def generate_presign_url(filename, expiration=3600):
    """Сгенерировать presigned URL для скачивания файла"""
    try:
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": BUCKET_NAME, "Key": filename},
            ExpiresIn=expiration
        )
        return url
    except Exception:
        return None
```

#### Few-shot промт

```text
Доработай код FastAPI-сервиса для S3, используя несколько примеров операций boto3.Пример 1 — список файлов:```pythonresponse = s3.list_objects_v2(Bucket=bucket_name)files = response.get("Contents", [])

Пример 2 — загрузка файла:
s3.upload_fileobj(file_obj, bucket_name, filename)

Пример 3 — удаление файла:
s3.delete_object(Bucket=bucket_name, Key=filename)

Пример 4 — presign-ссылка:
url = s3.generate_presigned_url(    "get_object",    Params={"Bucket": bucket_name, "Key": filename},    ExpiresIn=3600)

На основе этих примеров проверь и улучши функции:
- get_files;
- upload_file;
- delete_file;
- generate_presigned_url.

Добавь обработку ситуации, когда бакет пустой.  
Добавь простые сообщения об ошибках.  
Код должен оставаться понятным для лабораторной работы.
```

Модель обновила код s3_client.py и он был помещен в файл s3_client.py.

#### Промт на создание Readme

```text
Создай README.md для проекта FastAPI + Yandex Object Storage.

В README.md нужно описать:
1. Назначение проекта.
2. Структуру проекта.
3. Установку зависимостей.
4. Пример файла .env без реальных ключей.
5. Команду запуска через uvicorn.
6. Описание endpoint'ов:
   - GET /files
   - POST /upload
   - DELETE /files/{filename}
   - GET /presign/{filename}
```

Вывод модели можете посмотреть в файле generated-README.md

## Результат выполенения программы:
Модель смогла написать правильный код.

[![image.png](https://i.postimg.cc/Dz8dJ1sg/image.png)](https://postimg.cc/v1w6Cg0g)

[![image.png](https://i.postimg.cc/KjynHVW7/image.png)](https://postimg.cc/G8q8BMd9)
