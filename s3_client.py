import boto3
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Создание клиента S3 для Yandex Cloud
s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL", "https://storage.yandexcloud.net"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

# Имя бакета
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

if not BUCKET_NAME:
    raise EnvironmentError("Переменная окружения S3_BUCKET_NAME не установлена")


def list_files():
    """Получить список файлов в бакете. Возвращает пустой список, если бакет пуст."""
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        if "Contents" not in response:
            return []  # Бакет пуст
        return [item["Key"] for item in response["Contents"]]
    except Exception as e:
        raise Exception(f"Ошибка при получении списка файлов: {str(e)}")


def upload_file(file_obj, filename):
    """Загрузить файл в бакет"""
    try:
        s3.upload_fileobj(file_obj, BUCKET_NAME, filename)
    except Exception as e:
        raise Exception(f"Ошибка при загрузке файла: {str(e)}")


def delete_file(filename):
    """Удалить файл из бакета"""
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
    except Exception as e:
        raise Exception(f"Ошибка при удалении файла: {str(e)}")


def generate_presign_url(filename, expiration=3600):
    """
    Сгенерировать presigned URL для просмотра/скачивания файла.
    Возвращает URL или None, если файл не существует или недоступен.
    """
    try:
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": BUCKET_NAME, "Key": filename},
            ExpiresIn=expiration
        )
        return url
    except Exception:
        return None  # Например, если файла нет