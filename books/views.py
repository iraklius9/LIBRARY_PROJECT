from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.contrib import messages
from books.forms import BorrowForm, ReturnBookForm
from books.models import Book, Reservation, BookInstance, BorrowingHistory
from django.db import transaction

from users.models import CustomUser


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
        paginator = Paginator(books, 6)
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


@login_required
def staff(request):
    borrow_form = BorrowForm(request.POST or None)

    if request.method == 'POST':
        if borrow_form.is_valid():
            borrow_instance = borrow_form.save(commit=False)

            existing_borrow_instance = BookInstance.objects.filter(
                book=borrow_instance.book,
                borrower=borrow_instance.borrower,
                status='On loan'
            ).first()

            if existing_borrow_instance:
                error_message = (f"{borrow_instance.borrower} has already borrowed this book. Please return it before "
                                 f"borrowing again.")
                messages.error(request, error_message)
                return redirect('books:staff')

            if borrow_instance.returned_date and borrow_instance.returned_date < borrow_instance.borrowed_date:
                error_message = 'Returned date cannot be before borrowed date.'
                context = {'borrow_form': borrow_form, 'error_message': error_message}
                return render(request, 'staff.html', context)

            with transaction.atomic():
                borrow_instance.status = 'On loan'
                borrow_instance.save()

                Book.objects.filter(id=borrow_instance.book.id).update(stock_quantity=F('stock_quantity') - 1)

                messages.success(request, 'Book has been successfully marked as borrowed.')

                user_reservation = Reservation.objects.filter(
                    book=borrow_instance.book,
                    user=borrow_instance.borrower
                ).first()

                if user_reservation:
                    user_reservation.delete()
                    messages.info(request, 'Reservation has been automatically canceled.')

                return redirect('books:staff')

    context = {'borrow_form': borrow_form}
    return render(request, 'staff.html', context)


@login_required
def return_book(request):
    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            borrower = form.cleaned_data['borrower']
            returning_date = form.cleaned_data['returning_date']

            try:
                book_instance = BookInstance.objects.get(book=book, borrower=borrower, status='On loan')

                borrowing_date = book_instance.borrowed_date

                book_instance.book.stock_quantity += 1
                book_instance.book.save()

                book_instance.status = 'Returned'
                if returning_date:
                    book_instance.returned_date = returning_date
                book_instance.save()

                late_return = False
                if returning_date and returning_date > borrowing_date:
                    late_return = True

                BorrowingHistory.objects.create(
                    book_instance=book_instance,
                    book=book_instance.book,
                    borrower=borrower,
                    borrowing_date=borrowing_date,
                    returning_date=returning_date or timezone.now(),

                )

                if late_return:
                    messages.warning(request, 'Book returned late.')
                else:
                    messages.success(request, 'Book has been successfully marked as returned.')
            except BookInstance.DoesNotExist:
                messages.error(request, 'No matching book instance found for the given book and borrower.')
            return redirect('books:return_book')
    else:
        form = ReturnBookForm()

    return render(request, 'return_book.html', {'form': form})


@login_required
def reserve_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":

        user_reservation = Reservation.objects.filter(book=book, user=request.user).first()
        if not user_reservation:
            if book.stock_quantity > 0:
                book.stock_quantity -= 1
                book.save()
            else:
                messages.warning(request, 'No stock available for this book.')
                return redirect('books:book_detail', pk=book.pk)

            reservation = Reservation(
                book=book,
                user=request.user,
                reserved_at=timezone.now(),
                expires_at=timezone.now() + timedelta(days=1)
            )
            reservation.save()
            messages.success(request, 'Book reserved successfully.')
        else:
            messages.warning(request, 'You have already reserved this book.')

        return redirect('books:book_detail', pk=book.pk)
    return redirect('books:book_detail', pk=book.pk)


@login_required
def cancel_reservation(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user_reservation = Reservation.objects.filter(book=book, user=request.user).first()

    if user_reservation:
        book.stock_quantity += 1
        book.save()

        user_reservation.delete()

        messages.success(request, 'Reservation canceled successfully.')
    else:
        messages.error(request, 'You do not have a reservation for this book.')

    return redirect('books:book_detail', pk=book.pk)


@login_required
def check_reservations(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            user_reservations = Reservation.objects.filter(user=user)
            if user_reservations.exists():
                return render(request, 'reservation_check.html', {
                    'user_reservations': user_reservations,
                    'user_emails': CustomUser.objects.values_list('email', flat=True)
                })
            else:
                messages.info(request, 'This user does not have any reservations.')
                return render(request, 'reservation_check.html', {
                    'user_emails': CustomUser.objects.values_list('email', flat=True)
                })
        except CustomUser.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return render(request, 'reservation_check.html', {
                'user_emails': CustomUser.objects.values_list('email', flat=True)
            })

    return render(request, 'reservation_check.html', {
        'user_emails': CustomUser.objects.values_list('email', flat=True)
    })


@login_required
def check_borrowing(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            user_borrowings = BookInstance.objects.filter(borrower=user, status='On loan')
            if user_borrowings.exists():
                return render(request, 'borrowing_check.html', {
                    'user_borrowings': user_borrowings,
                    'user_emails': CustomUser.objects.values_list('email', flat=True)
                })
            else:
                messages.info(request, 'This user does not have any borrowed books.')
                return render(request, 'borrowing_check.html', {
                    'user_emails': CustomUser.objects.values_list('email', flat=True)
                })
        except CustomUser.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return render(request, 'borrowing_check.html', {
                'user_emails': CustomUser.objects.values_list('email', flat=True)
            })

    return render(request, 'borrowing_check.html', {
        'user_emails': CustomUser.objects.values_list('email', flat=True)
    })
