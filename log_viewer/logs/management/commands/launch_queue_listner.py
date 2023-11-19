from django.core.management.base import BaseCommand
from logs.utils.queue_listener import LogsCreatedListener
class Command(BaseCommand):
    help = 'Launches Listener for user_created message : Kafka'
    def handle(self, *args, **options):
        td = LogsCreatedListener()
        td.start()
        self.stdout.write("Started Consumer Thread")