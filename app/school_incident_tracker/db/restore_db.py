import boto3
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def restore_db_from_s3():
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME")
    db_path_source = "db.sqlite3"
    db_path_target = str(settings.DATABASES["default"]["NAME"])

    try:
        s3_client.download_file(bucket_name, db_path_source, db_path_target)
        logger.info(f"Database restored from S3: {bucket_name}/{db_path_source}")
    except Exception as e:
        logger.error(f"Failed to restore database: {e}")
