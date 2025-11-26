from minio import Minio
from minio.error import S3Error
import os
import io
from typing import Optional

class MinioClient:
    def __init__(self):
        self.client = Minio(
            endpoint=os.getenv("MINIO_ENDPOINT", "minio:9000"),
            access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
            secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
            secure=False
        )
        self.bucket_name = "film-club"
        self._ensure_bucket_and_structure_exists()

    def _ensure_bucket_and_structure_exists(self):
        """Создает бакет и структуру папок"""
        try:
            # Создаем бакет если не существует
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"Bucket '{self.bucket_name}' created successfully")
            
            # Базовая структура папок - ТОЛЬКО events и submissions
            base_folders = [        
                "events/",           # Афиши мероприятий
                "submissions/"       # Афиши фильмов (заявки)
            ]
            
            for folder in base_folders:
                self._create_folder(folder)
            print("Base folder structure created: events/, submissions/")
                        
        except S3Error as err:
            print(f"Error creating bucket structure: {err}")

    def _create_folder(self, folder_path: str):
        """Создает папку в бакете"""
        try:
            # Используем BytesIO для создания объекта с методом read
            empty_data = io.BytesIO(b'')
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=folder_path,
                data=empty_data,
                length=0
            )
            print(f"Folder '{folder_path}' created")
        except S3Error as err:
            if err.code != "NoSuchBucket":
                print(f"Note: Folder '{folder_path}' may already exist")

    def upload_event_poster(self, file_data: bytes, file_name: str) -> str:
        """Загружает постер мероприятия в папку events"""
        return self.upload_file(file_data, file_name, "events")

    def upload_submission(self, file_data: bytes, file_name: str) -> str:
        """Загружает афишу фильма в папку submissions"""
        return self.upload_file(file_data, file_name, "submissions")

    def upload_file(self, file_data: bytes, file_name: str, folder: str = "") -> str:
        """
        Универсальный метод загрузки файла
        """
        try:
            object_name = f"{folder}/{file_name}" if folder else file_name
            
            # Конвертируем bytes в BytesIO
            data_stream = io.BytesIO(file_data)
            
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=data_stream,
                length=len(file_data),
                content_type=self._get_content_type(file_name)
            )
            
            return f"http://localhost:9000/{self.bucket_name}/{object_name}"
            
        except S3Error as err:
            print(f"Error uploading file: {err}")
            raise

    def _get_content_type(self, filename: str) -> str:
        """Определяет content-type по расширению файла"""
        extension = filename.lower().split('.')[-1] if '.' in filename else ''
        content_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'pdf': 'application/pdf',
            'txt': 'text/plain'
        }
        return content_types.get(extension, 'application/octet-stream')

    def download_file(self, file_name: str, folder: str = "") -> bytes:
        """
        Скачивает файл из MinIO
        """
        try:
            object_name = f"{folder}/{file_name}" if folder else file_name
            response = self.client.get_object(self.bucket_name, object_name)
            # Читаем данные и сразу закрываем соединение
            file_data = response.read()
            response.close()
            response.release_conn()
            return file_data
        except S3Error as err:
            print(f"Error downloading file: {err}")
            raise

    def list_files(self, folder: str = "") -> list:
        """
        Список файлов в папке
        """
        try:
            prefix = f"{folder}/" if folder else ""
            objects = self.client.list_objects(self.bucket_name, prefix=prefix, recursive=True)
            # Фильтруем пустые папки (объекты с нулевой длиной)
            files = []
            for obj in objects:
                if obj.size > 0:  # Исключаем пустые папки
                    files.append(obj.object_name)
            return files
        except S3Error as err:
            print(f"Error listing files: {err}")
            return []

    def delete_file(self, file_name: str, folder: str = "") -> bool:
        """Удаляет файл из MinIO"""
        try:
            object_name = f"{folder}/{file_name}" if folder else file_name
            self.client.remove_object(self.bucket_name, object_name)
            return True
        except S3Error as err:
            print(f"Error deleting file: {err}")
            return False

    def get_file_url(self, file_name: str, folder: str = "") -> str:
        """Возвращает URL для доступа к файлу"""
        object_name = f"{folder}/{file_name}" if folder else file_name
        return f"http://localhost:9000/{self.bucket_name}/{object_name}"

    def file_exists(self, file_name: str, folder: str = "") -> bool:
        """Проверяет существует ли файл"""
        try:
            object_name = f"{folder}/{file_name}" if folder else file_name
            self.client.stat_object(self.bucket_name, object_name)
            return True
        except S3Error:
            return False

# Создаем глобальный экземпляр клиента
minio_client = MinioClient()