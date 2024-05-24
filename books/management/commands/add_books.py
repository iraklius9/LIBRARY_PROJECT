import random
from django.core.management.base import BaseCommand
from faker import Faker
from books.models import Author, Genre, Book


class Command(BaseCommand):
    help = 'Generate random books'

    def handle(self, *args, **kwargs):
        faker = Faker()
        genres = ['Fiction', 'Non-fiction', 'Science', 'History', 'Fantasy', 'Biography', 'Children', 'Romance']
        author_objs = [Author.objects.create(name=faker.name()) for _ in range(100)]
        genre_objs = [Genre.objects.get_or_create(name=genre)[0] for genre in genres]
        books = []

        for _ in range(1000):
            title = faker.sentence(nb_words=4)
            author = random.choice(author_objs)
            genre = random.choice(genre_objs)
            publication_date = faker.date_between(start_date='-50y', end_date='today')
            stock_quantity = random.randint(1, 20)
            books.append(
                Book(title=title, author=author, publication_date=publication_date, stock_quantity=stock_quantity))
            books[-1].save()
            books[-1].genre.set([genre])

        self.stdout.write(self.style.SUCCESS('Successfully generated books'))
