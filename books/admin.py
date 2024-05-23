from django.contrib import admin
from .models import Book, Author, Genre, BookInstance, BorrowingHistory, Reservation


class BorrowingHistoryInline(admin.TabularInline):
    model = BorrowingHistory
    extra = 0


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'borrower', 'borrowed_date', 'returned_date', 'status']
    list_filter = ['status', 'borrowed_date', 'returned_date']
    search_fields = ['book__title', 'borrower__email']
    date_hierarchy = 'borrowed_date'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Exclude book instances with status 'Returned'
        return qs.exclude(status='Returned')


class AuthorFilter(admin.SimpleListFilter):
    title = 'Author'
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        authors = Author.objects.all()
        return [(author.id, author.name) for author in authors]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(author__id=self.value())
        return queryset


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
    list_display = ['title', 'author', 'publication_date', 'stock_quantity', 'get_num_borrowed', 'get_num_published',
                    'image']
    list_filter = ['publication_date', AuthorFilter, GenreFilter]
    search_fields = ['title', 'author__name']
    inlines = [BookInstanceInline, BorrowingHistoryInline]

    def get_num_borrowed(self, obj):
        return obj.num_borrowed()

    get_num_borrowed.short_description = 'Times Borrowed'

    def get_num_published(self, obj):
        return obj.num_published()

    get_num_published.short_description = 'Total Published'


class BorrowingHistoryAdmin(admin.ModelAdmin):
    list_display = ['book_instance', 'borrower', 'borrowing_date', 'returning_date']
    list_filter = ['borrowing_date']
    search_fields = ['book__title', 'borrower__email']
    date_hierarchy = 'borrowing_date'


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'reserved_at', 'expires_at')
    list_filter = ('reserved_at', 'expires_at')
    search_fields = ('user__username', 'book__title')


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(BorrowingHistory, BorrowingHistoryAdmin)
admin.site.register(Reservation, ReservationAdmin)
