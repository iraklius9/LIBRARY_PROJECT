# books/management/commands/check_expired_reservations.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from books.models import Book, Reservation


class Command(BaseCommand):
    help = 'Increase stock count of books that have expired reservations'

    def handle(self, *args, **kwargs):
        expired_reservations = Reservation.objects.filter(expires_at__lt=timezone.now())
        for reservation in expired_reservations:
            book = reservation.book
            book.stock_quantity += 1
            book.save()
            reservation.delete()
            self.stdout.write(self.style.SUCCESS(f'Stock increased for book {book.title}'))
