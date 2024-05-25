from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from books.models import BookInstance


class Command(BaseCommand):
    help = 'Sends reminder emails for overdue books'

    def handle(self, *args, **options):
        overdue_books = BookInstance.objects.filter(status='On loan', returned_date__lt=timezone.now())
        for book_instance in overdue_books:
            borrower_email = book_instance.borrower.email
            send_mail(
                'Reminder: Return Overdue Book',
                'Dear borrower, please return the book "{}" as soon as possible.'.format(book_instance.book.title),
                'library@gmail.com',
                [borrower_email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('Reminder email sent to {}'.format(borrower_email)))
