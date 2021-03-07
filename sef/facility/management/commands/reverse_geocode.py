"""Reverse Geocode."""
from django.core.management.base import BaseCommand

from sef.facility.tasks.utils import geocode_reverse


class Command(BaseCommand):
    """Reverse Geocode; just a convinient helper."""

    help = 'Reverse Geocode'

    def add_arguments(self, parser):
        """Add args / flags to the management command."""
        parser.add_argument(
            '-f', '--file',
            help='File with LatLong')

    def handle(self, *args, **options):
        """Entry point for the Reverse Geocode command."""
        reverse_file = options.get('file')

        geocode_reverse(reverse_file=reverse_file)
        self.stdout.write(self.style.SUCCESS('Reverse Geocode Successful'))
