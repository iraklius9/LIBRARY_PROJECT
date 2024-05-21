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

