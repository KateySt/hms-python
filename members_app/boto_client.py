from io import BytesIO
from pathlib import Path
from typing import Union

import boto3
from django.conf import settings


class S3BucketService:
    def __init__(
            self,
            bucket_name: str,
            access_key: str,
            secret_key: str,
            endpoint: str,
    ) -> None:
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key

    def create_s3_client(self) -> boto3.client:
        client = boto3.client(
            "s3",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            aws_session_token=None,
            endpoint_url=self.endpoint,
            config=boto3.session.Config(signature_version='s3v4'),
            verify=False,
        )
        return client

    def create_bucket_if_not_exists(self) -> None:
        client = self.create_s3_client()
        try:
            client.head_bucket(Bucket=self.bucket_name)
        except:
            client.create_bucket(Bucket=self.bucket_name)

    def upload_file_object(
            self,
            prefix: str,
            source_file_name: str,
            content: Union[str, bytes],
    ) -> str:
        client = self.create_s3_client()
        destination_path = str(Path(prefix, source_file_name))

        if isinstance(content, bytes):
            buffer = BytesIO(content)
        else:
            buffer = BytesIO(content.encode("utf-8"))

        client.upload_fileobj(buffer, self.bucket_name, destination_path)
        return destination_path

    def get_file_url(self, file_path: str, expiration: int = 3600) -> str:
        client = self.create_s3_client()
        url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': file_path
            },
            ExpiresIn=expiration
        )
        return url

    def delete_file_object(self, file_path: str) -> None:
        client = self.create_s3_client()
        client.delete_object(Bucket=self.bucket_name, Key=file_path)


def s3_bucket_service_factory() -> S3BucketService:
    service = S3BucketService(
        bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
        access_key=settings.AWS_ACCESS_KEY_ID,
        secret_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint=settings.AWS_S3_ENDPOINT_URL
    )
    service.create_bucket_if_not_exists()
    return service