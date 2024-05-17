from django.shortcuts import render
from books.models import Book


def library_page(request):
    books = Book.objects.all()
    return render(request, 'library.html', {'books': books})
