from django.core.management.base import BaseCommand
from django.utils import timezone
from random import choice
from string import ascii_letters, digits
from books.models import Book, Author, Genre
import random
import datetime


class Command(BaseCommand):
    help = 'Add 1000 random books to the system'

    def handle(self, *args, **kwargs):
        authors = Author.objects.all()
        genres = Genre.objects.all()

        for _ in range(1000):
            title = ''.join(random.choices(ascii_letters + digits, k=10))
            author = choice(authors)
            genre = choice(genres)
            publication_date = timezone.now() - datetime.timedelta(
                days=random.randint(1, 3650))
            stock_quantity = random.randint(1, 100)

            Book.objects.create(title=title, author=author, genre=genre, publication_date=publication_date,
                                stock_quantity=stock_quantity)

        self.stdout.write(self.style.SUCCESS('Successfully added 1000 random books'))
