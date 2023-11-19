# run_custom_server.py
# logs/management/commands/runserver3000.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run Django development server on port 3000'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Django development server on port 3000...'))

        # Your custom logic to start the server on port 3000
        from django.core.management import call_command
        call_command('runserver', '3000')