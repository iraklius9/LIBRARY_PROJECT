from django.db import models
from django.conf import settings
from django.utils import timezone


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    title = models.CharField(max_length=200)
    publication_date = models.DateField()
    stock_quantity = models.IntegerField()
    image = models.ImageField(upload_to='book_images', null=True, blank=True, default='book_images/2.jpg')

    def __str__(self):
        return self.title

    def num_borrowed(self):
        return self.bookinstance_set.filter(status='On loan').count()

    def num_published(self):
        return self.bookinstance_set.count()


class BookInstance(models.Model):
    STATUS_CHOICES = [

        ('On loan', 'On loan'),
        ('Maintenance', 'Maintenance'),
        ('Reserved', 'Reserved'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    borrowed_date = models.DateField(null=True, blank=True)
    returned_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Maintenance')

    def __str__(self):
        return f'{self.book.title}'


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.name} reserved {self.book.title}"

    @property
    def is_expired(self):
        return self.expires_at < timezone.now()
