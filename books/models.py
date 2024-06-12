from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from books.choices import STATUS_CHOICES


class Genre(models.Model):
    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")


class Author(models.Model):
    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class Book(models.Model):
    author = models.ForeignKey(Author, verbose_name=_("Author"), on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre, verbose_name=_("Genre"))
    title = models.CharField(_("Title"), max_length=200)
    publication_date = models.DateField(_("Publication Date"))
    stock_quantity = models.IntegerField(_("Stock Quantity"))
    image = models.ImageField(_("Image"), upload_to='book_images', null=True, blank=True, default='book_images/2.jpg')

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

    def num_late_returns(self, obj):
        return BorrowingHistory.objects.filter(book=obj, late_return=True).count()

    num_late_returns.short_description = 'Late Returns'

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")


class BookInstance(models.Model):
    book = models.ForeignKey(Book, verbose_name=_("Book"), on_delete=models.CASCADE)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Borrower"), on_delete=models.SET_NULL,
                                 null=True, blank=True)
    borrowed_date = models.DateField(_("Borrowed Date"), null=False, blank=False)
    returned_date = models.DateField(_("Returned Date"), null=False, blank=False)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='On loan')

    def __str__(self):
        return f'{self.book.title}'

    class Meta:
        verbose_name = _("Book Instance")
        verbose_name_plural = _("Book Instances")


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name=_("Book"), on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(_("Reserved At"), auto_now_add=True)
    expires_at = models.DateTimeField(_("Expires At"))

    @property
    def is_expired(self):
        return self.expires_at < timezone.now()

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")


class BorrowingHistory(models.Model):
    book_instance = models.ForeignKey(BookInstance, verbose_name=_("Book Instance"), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name=_("Book"), on_delete=models.CASCADE)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Borrower"), on_delete=models.CASCADE)
    borrowing_date = models.DateTimeField(_("Borrowing Date"))
    returning_date = models.DateTimeField(_("Returning Date"), null=True, blank=True)
    late_return = models.BooleanField(_("Late Return"), default=False)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower.username} on {self.borrowing_date}"

    class Meta:
        verbose_name = _("Borrowing History")
        verbose_name_plural = _("Borrowing Histories")


class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name=_("Book"), on_delete=models.CASCADE)
    added_at = models.DateTimeField(_("Added At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Wish List")
        verbose_name_plural = _("Wish Lists")
