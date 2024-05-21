from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from books.models import Book
from books.forms import BookSearchForm


def library(request):
    query = request.GET.get('query', '')
    author = request.GET.get('author', '')
    genre = request.GET.get('genre', '')

    # Filter books based on query parameters
    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query)
    if author:
        books = books.filter(author__name__icontains=author)  # Assuming 'name' is the field on the Author model
    if genre:
        books = books.filter(genre__name__icontains=genre)  # Assuming 'name' is the field on the Genre model

    # Check if filters are applied
    filters_applied = any([query, author, genre])

    # Pagination
    page = request.GET.get('page')
    if not filters_applied:
        paginator = Paginator(books, 2)  # Show 2 books per page
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            books = paginator.page(1)
            page = 1
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            books = paginator.page(paginator.num_pages)
            page = paginator.num_pages
        else:
            page = int(page)
    else:
        page = None

    context = {
        'books': books,
        'filters_applied': filters_applied,
        'page': page,
    }
    return render(request, 'library.html', context)


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'book': book})


def staff(request):
    return render(request, 'staff.html')
