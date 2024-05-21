from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from books.models import Book, Reservation


@login_required
def library(request):
    query = request.GET.get('query', '')
    author = request.GET.get('author', '')
    genre = request.GET.get('genre', '')

    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query)
    if author:
        books = books.filter(author__name__icontains=author)
    if genre:
        books = books.filter(genre__name__icontains=genre)

    filters_applied = any([query, author, genre])

    page = request.GET.get('page')
    if not filters_applied:
        paginator = Paginator(books, 2)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:

            books = paginator.page(1)
            page = 1
        except EmptyPage:

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
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user_reservation = Reservation.objects.filter(book=book, user=request.user).first()
    user_has_reservation = bool(user_reservation)
    expiration_date = user_reservation.expires_at.strftime('%Y-%m-%d %H:%M:%S') if user_reservation else None

    if user_reservation and user_reservation.expires_at < timezone.now():
        user_reservation.delete()
        user_reservation = None
        expiration_date = None
        user_has_reservation = False

    context = {
        'book': book,
        'user_has_reservation': user_has_reservation,
        'expiration_date': expiration_date,
    }
    return render(request, 'book_detail.html', context)


def staff(request):
    return render(request, 'staff.html')


@login_required
def reserve_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        user_reservation = Reservation.objects.filter(book=book, user=request.user).first()
        if not user_reservation:
            book.stock_quantity -= 1
            book.save()

            reservation = Reservation(
                book=book,
                user=request.user,
                reserved_at=timezone.now(),
                expires_at=timezone.now() + timedelta(days=1)
            )
            reservation.save()

        return redirect('books:book_detail', pk=book.pk)
    return redirect('books:book_detail', pk=book.pk)


@login_required
def return_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        reservation = Reservation.objects.filter(book=book, user=request.user).first()
        if reservation:
            reservation.delete()
        return redirect('books:book_detail', pk=book.id)
    return redirect('books:book_detail', pk=book.id)
