import io
import os
from io import BytesIO
from minio import Minio
from dotenv import load_dotenv

# загрузка переменных окружения из файла .env
load_dotenv()


# класс для взаимодействия с базой данных
class MinioRepository:

    # конструктор класса, который вызывается при создании объекта
    def __init__(self):
        # создаем подключение к MinIO
        self.client = Minio(
            endpoint=os.getenv('MINIO_SERVER'),
            access_key=os.getenv('MINIO_ACCESS_KEY'),
            secret_key=os.getenv('MINIO_SECRET_KEY'),
            secure=False
        )
        # указываем имя бакета, в котором хранятся файлы
        self.bucket_name = os.getenv('MINIO_BUCKET_NAME')

        # если бакета не существует, то создаем его
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    # метод сохраняет изображение и возвращает URL-адрес файла
    def upload_image(self, name: str, file: bytes) -> str:
        # загружаем объект на сервер MinIO
        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=name,
            data=io.BytesIO(file),
            length=len(file),
        )
        # возвращаем ссылку на изображение
        return f'http://127.0.0.1:5000/image/{name}'

    # получить изображение с сервера Minio
    def get_image(self, filename: str) -> BytesIO:
        response = self.client.get_object(
            bucket_name=self.bucket_name,
            object_name=filename
        )
        return io.BytesIO(response.data)
