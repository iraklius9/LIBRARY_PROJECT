# books/management/commands/remove_expired_reservations.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from books.models import Reservation


class Command(BaseCommand):
    help = 'Removes expired book reservations'

    def handle(self, *args, **kwargs):
        expired_reservations = Reservation.objects.filter(expires_at__lt=timezone.now())
        count = expired_reservations.count()
        expired_reservations.delete()
        self.stdout.write(f'Successfully removed {count} expired reservations.')
