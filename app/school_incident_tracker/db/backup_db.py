import boto3
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def backup_db_to_s3():
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME")
    db_path_source = str(settings.DATABASES["default"]["NAME"])
    db_path_target = "db.sqlite3"

    try:
        s3_client.upload_file(db_path_source, bucket_name, db_path_target)
    except Exception as e:
        logger.error(f"Failed to back up database: {e}")
