# from django.contrib import admin
# from django.db.models import Count, Q
# from .models import Book, Author, Genre, BookInstance
#
#
# class BookInstanceInline(admin.TabularInline):
#     model = BookInstance
#     extra = 0
#
#
# class GenreFilter(admin.SimpleListFilter):
#     title = 'genre'
#     parameter_name = 'genre'
#
#     def lookups(self, request, model_admin):
#         genres = Genre.objects.all()
#         return [(g.id, g.name) for g in genres]
#
#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(genre__id=self.value())
#         return queryset
#
#
# class AuthorFilter(admin.SimpleListFilter):
#     title = 'author'
#     parameter_name = 'author'
#
#     def lookups(self, request, model_admin):
#         authors = Author.objects.all()
#         return [(a.id, a.name) for a in authors]
#
#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(author__id=self.value())
#         return queryset
#
#
# class BookAdmin(admin.ModelAdmin):
#     list_display = ['title', 'author', 'publication_date', 'stock_quantity', 'num_borrowed']
#     list_filter = ['publication_date', AuthorFilter, GenreFilter]
#     search_fields = ['title', 'author__name']
#     inlines = [BookInstanceInline]
#
#     def num_borrowed(self, obj):
#         return obj.bookinstance_set.filter(borrower__isnull=False, returned_date__isnull=True).count()
#
#     num_borrowed.short_description = 'Times Borrowed'
#
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         queryset = queryset.annotate(
#             num_borrowed=Count('bookinstance',
#                                filter=Q(bookinstance__borrower__isnull=False, bookinstance__returned_date__isnull=True))
#         )
#         return queryset
#
#
# admin.site.register(Book, BookAdmin)
# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(BookInstance)

from django.contrib import admin
from .models import Book, Author, Genre, BookInstance


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


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
    list_display = ['title', 'author', 'publication_date', 'stock_quantity', 'get_num_borrowed', 'get_num_published', 'image']
    list_filter = ['publication_date', AuthorFilter, GenreFilter]
    search_fields = ['title', 'author__name']
    inlines = [BookInstanceInline]

    def get_num_borrowed(self, obj):
        return obj.num_borrowed()

    get_num_borrowed.short_description = 'Times Borrowed'

    def get_num_published(self, obj):
        return obj.num_published()

    get_num_published.short_description = 'Total Published'


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance)

