"""
WSGI config for school_incident_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
import signal
import django
from django.core.wsgi import get_wsgi_application
from school_incident_tracker.db.restore_db import restore_db_from_s3
from school_incident_tracker.db.backup_db import backup_db_to_s3

# Restore database from S3 if the SQLite DB doesn't exist
if __name__ == "__main__":
    if not os.path.exists("db.sqlite3"):  # Prevent overwriting an existing local DB
        restore_db_from_s3()

# Set up Django environment before proceeding
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_incident_tracker.settings")
django.setup()


# Signal handler to backup the DB before shutting down
def backup_db_handler(signal, frame):
    backup_db_to_s3()
    sys.exit(0)


signal.signal(signal.SIGTERM, backup_db_handler)

# Get the WSGI application
application = get_wsgi_application()
