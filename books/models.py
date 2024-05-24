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
        return BorrowingHistory.objects.filter(book=self).count()

    def num_published(self):
        return self.bookinstance_set.filter(status='On loan').count()

    def total_quantity(self):
        reserved_books = Reservation.objects.filter(book=self).count()
        return self.stock_quantity + self.num_published() + reserved_books

    def reserved_quantity(self):
        return Reservation.objects.filter(book=self).count()


class BookInstance(models.Model):
    STATUS_CHOICES = [

        ('On loan', 'On loan'),
        ('Maintenance', 'Maintenance'),
        ('Reserved', 'Reserved'),
        ('Returned', 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    borrowed_date = models.DateField(null=False, blank=False)
    returned_date = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='On loan')

    def __str__(self):
        return f'{self.book.title}'


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @property
    def is_expired(self):
        return self.expires_at < timezone.now()


class BorrowingHistory(models.Model):
    book_instance = models.ForeignKey(BookInstance, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Add this line
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    borrowing_date = models.DateTimeField()
    returning_date = models.DateTimeField(null=True, blank=True)


def __str__(self):
    return f"{self.book.title} borrowed by {self.borrower.username} on {self.borrowing_date}"
