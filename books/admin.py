from django.contrib import admin
from django.db import models
from django.db.models import Count

from books.forms import BorrowingHistoryAdminForm
from books.models import Book, Author, Genre, BookInstance, BorrowingHistory, Reservation, WishList


class BorrowingHistoryInline(admin.TabularInline):
    model = BorrowingHistory
    extra = 0


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

    list_per_page = 10


class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'borrower', 'borrowed_date', 'returned_date', 'status']
    list_filter = ['status', 'borrowed_date', 'returned_date']
    search_fields = ['book__title', 'borrower__email']
    date_hierarchy = 'borrowed_date'
    autocomplete_fields = ['book', 'borrower']

    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(status='Returned')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'book':
            kwargs['queryset'] = db_field.related_model.objects.filter(stock_quantity__gt=0)
        elif db_field.name == 'borrower':
            kwargs['queryset'] = db_field.related_model.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            book = obj.book
            if book.stock_quantity > 0:
                book.stock_quantity -= 1
                book.save()
        super().save_model(request, obj, form, change)


class GenreFilter(admin.SimpleListFilter):
    title = 'Genre'
    parameter_name = 'genre'

    def lookups(self, request, model_admin):
        genres = Genre.objects.all()
        return [(genre.id, genre.name) for genre in genres]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(genre__id=self.value())
        return queryset


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'publication_date', 'total_quantity', 'stock_quantity',
                    'get_num_published', 'reserved_quantity', 'get_num_borrowed', 'late_returned']
    list_filter = ['publication_date', GenreFilter]
    search_fields = ['title', 'author__name']
    inlines = [BookInstanceInline, BorrowingHistoryInline]
    list_per_page = 6
    raw_id_fields = ['author', 'genre']
    ordering = ['id']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            num_late_returned=Count('bookinstance__borrowinghistory',
                                    filter=models.Q(bookinstance__borrowinghistory__late_return=True))
        )
        return qs

    def late_returned(self, obj):
        return obj.num_late_returned

    late_returned.admin_order_field = 'num_late_returned'
    late_returned.short_description = 'Late Returned'

    def get_num_borrowed(self, obj):
        return obj.num_borrowed()

    get_num_borrowed.short_description = 'Times Borrowed'

    def get_num_published(self, obj):
        return obj.num_published()

    get_num_published.short_description = 'Now Borrowed'


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'reserved_at', 'expires_at')
    list_filter = ('reserved_at', 'expires_at')
    search_fields = ('user__username', 'book__title')

    list_per_page = 10


class BorrowingHistoryAdmin(admin.ModelAdmin):
    form = BorrowingHistoryAdminForm
    list_display = ['book', 'borrower', 'borrowing_date', 'returning_date', 'book_instance_returned_date', ]
    list_filter = ['borrowing_date']
    search_fields = ['book__title', 'borrower__email']
    date_hierarchy = 'borrowing_date'
    raw_id_fields = ['book', 'borrower']

    list_per_page = 10

    def book_instance_returned_date(self, obj):
        return obj.book_instance.returned_date

    book_instance_returned_date.short_description = 'Due Date'


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'book']
    search_fields = ['user__username', 'book__title']
    list_per_page = 10


admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(BorrowingHistory, BorrowingHistoryAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(WishList, WishlistAdmin)
