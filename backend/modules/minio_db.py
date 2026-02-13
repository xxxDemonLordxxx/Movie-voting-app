import os
import io
import json
from datetime import timedelta
from minio import Minio
from minio.error import S3Error
import uuid

# Конфигурация из переменных окружения
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_PUBLIC_ENDPOINT = os.getenv("MINIO_PUBLIC_ENDPOINT", "observational.website")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_SECURE = os.getenv("MINIO_SECURE", "False").lower() == "true"

# Названия папок (префиксов)
EVENTS_FOLDER = "events"
SUBMISSIONS_FOLDER = "submissions"

class MinioClient:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE
        )
        self._init_bucket()
    
    def _init_bucket(self):
        """Инициализация бакета и создание папок"""
        try:
            # Создаем бакет если не существует
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
            
            # УСТАНАВЛИВАЕМ ПОЛИТИКУ ДОСТУПА (публичный read-only)
            public_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{self.bucket_name}/*"]
                    }
                ]
            }
            
            try:
                self.client.set_bucket_policy(
                    self.bucket_name,
                    json.dumps(public_policy)
                )
            except Exception as e:
                print(f"Note: Could not set public policy (might already exist): {e}")
            
            # Создаем дефолтные папки
            for folder in [EVENTS_FOLDER, SUBMISSIONS_FOLDER]:
                folder_path = f"{folder}/"
                try:
                    folder_stream = io.BytesIO(b"")
                    self.client.put_object(
                        self.bucket_name,
                        folder_path,
                        folder_stream,
                        length=0
                    )
                except S3Error:
                    pass
                    
        except S3Error as e:
            print(f"Error initializing MinIO bucket: {e}")
        
    def upload_file(self, file_data: bytes, filename: str, folder: str) -> str:
        """Загружает файл и возвращает его уникальное имя"""
        # Генерируем уникальное имя файла
        ext = filename.split('.')[-1] if '.' in filename else 'bin'
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        object_name = f"{folder}/{unique_filename}"
        
        # Определяем content type
        content_type = self._get_content_type(ext)
        
        # Преобразуем bytes в BytesIO
        file_stream = io.BytesIO(file_data)
        file_length = len(file_data)
        
        # Загружаем в MinIO
        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=file_stream,
            length=file_length,
            content_type=content_type
        )
        
        return unique_filename
    
    def _get_content_type(self, ext: str) -> str:
        """Определяет content type по расширению файла"""
        ext = ext.lower()
        if ext in ['jpg', 'jpeg']:
            return 'image/jpeg'
        elif ext == 'png':
            return 'image/png'
        elif ext == 'gif':
            return 'image/gif'
        elif ext == 'webp':
            return 'image/webp'
        elif ext == 'svg':
            return 'image/svg+xml'
        else:
            return 'application/octet-stream'
    
    def get_file_url(self, file_id: str, folder: str, expires: int = 3600) -> str:
        """Генерирует временную ссылку на файл"""
        full_object_name = f"{folder}/{file_id}"
        
        url = self.client.presigned_get_object(
            bucket_name=self.bucket_name,
            object_name=full_object_name,
            expires=timedelta(seconds=expires)
        )
        
        return url
    
    def get_file_data(self, file_id: str, folder: str) -> bytes:
        """Получает данные файла"""
        full_object_name = f"{folder}/{file_id}"
        
        try:
            response = self.client.get_object(
                bucket_name=self.bucket_name,
                object_name=full_object_name
            )
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as e:
            raise Exception(f"Failed to get file: {e}")
    
    def delete_file(self, file_id: str, folder: str) -> bool:
        """Удаляет файл"""
        full_object_name = f"{folder}/{file_id}"
        
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=full_object_name
            )
            return True
        except S3Error:
            return False
    
    def get_file_url(self, file_id: str, folder: str) -> str:
        return f"http://{MINIO_PUBLIC_ENDPOINT}/{self.bucket_name}/{folder}/{file_id}"
    
    def file_exists(self, file_id: str, folder: str) -> bool:
        """Проверяет существует ли файл"""
        full_object_name = f"{folder}/{file_id}"
        try:
            self.client.stat_object(
                bucket_name=self.bucket_name,
                object_name=full_object_name
            )
            return True
        except S3Error:
            return False


# Глобальный клиент
minio_client = None

def init_minio(bucket_name: str = "images-bucket"):
    """Инициализация глобального клиента MinIO"""
    global minio_client
    minio_client = MinioClient(bucket_name)
    print(f"MinIO initialized with bucket: {bucket_name}")
    return minio_client

def get_minio_client() -> MinioClient:
    """Получить глобальный клиент MinIO"""
    if minio_client is None:
        raise RuntimeError("MinIO client not initialized. Call init_minio() first.")
    return minio_client