# populate_logs_from_csv.py

import os
import json
import csv
from datetime import datetime

# Set the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'log_viewer.settings')  # Change 'project.settings' to your actual project settings module

import django
from django.utils import timezone
django.setup()

from logs.models import LogData

def populate_logs_from_log_file(log_file_path):
    with open(log_file_path, 'r') as file:
        for line in file:
            log_data = json.loads(line)
            log_entry = LogData.objects.create(
                level=log_data["level"],
                message=log_data["message"],
                resourceId=log_data["resourceId"],
                timestamp=datetime.strptime(log_data["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc),
                traceId=log_data["traceId"],
                spanId=log_data["spanId"],
                commit=log_data["commit"],
                parentResourceId=log_data["metadata"].get("parentResourceId")
            )
            log_entry.save()

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # .log file needs to be in the same directory as populate_logs_from_log.py
    csv_file_path = os.path.join(BASE_DIR, 'dummy_logs.log')
    print(csv_file_path)
    populate_logs_from_log_file(csv_file_path)
