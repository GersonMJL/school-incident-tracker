from django.core.management.base import BaseCommand
from school_incident_tracker.db.backup_db import backup_db_to_s3


class Command(BaseCommand):
    help = "Back up SQLite database to S3"

    def handle(self, *args, **kwargs):
        backup_db_to_s3()
        self.stdout.write(self.style.SUCCESS("Database backed up to S3"))
