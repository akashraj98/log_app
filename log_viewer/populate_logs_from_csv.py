# populate_logs_from_csv.py

import os
import csv
from datetime import datetime

# Set the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'log_viewer.settings')  # Change 'project.settings' to your actual project settings module

import django
from django.utils import timezone
django.setup()

from logs.models import LogData
def populate_logs_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            log_entry = LogData.objects.create(
                level=row["level"],
                message=row["message"],
                resourceId=row["resourceId"],
                timestamp=datetime.strptime(row["timestamp"], "%Y-%m-%dT%H:%M:%SZ"),
                traceId=row["traceId"],
                spanId=row["spanId"],
                commit=row["commit"],
                parentResourceId=row.get("parentResourceId")
            )
            log_entry.save()

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # sample.csv file needs to be in the same directory as populate_logs_from_csv.py
    csv_file_path = os.path.join(BASE_DIR, 'sample.csv')
    print(csv_file_path)
    populate_logs_from_csv(csv_file_path)
