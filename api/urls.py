from django.urls import path
from .views import AuthorListCreate, GenreListCreate, BookListCreate, BookRetrieveUpdateDestroy, \
    ReservationCreateAPIView, ReservationCheckAPIView, MostPopularBooksAPIView, \
    BooksBorrowedLastYearAPIView, TopLateReturnedBooksAPIView, TopLateReturnedUsersAPIView, BookReturnAPIView

urlpatterns = [
    path('authors/', AuthorListCreate.as_view(), name='author-list-create'),
    path('genres/', GenreListCreate.as_view(), name='genre-list-create'),
    path('books/', BookListCreate.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroy.as_view(), name='book-retrieve-update-destroy'),
    path('reserve/', ReservationCreateAPIView.as_view(), name='api_reserve_book'),
    path('check-reservation/', ReservationCheckAPIView.as_view(), name='api_check_reservation'),
    path('most-popular-books/', MostPopularBooksAPIView.as_view(), name='most-popular-books'),
    path('books-borrowed-last-year/', BooksBorrowedLastYearAPIView.as_view(), name='books-borrowed-last-year'),
    path('top-late-returned-books/', TopLateReturnedBooksAPIView.as_view(), name='top-late-returned-books'),
    path('top-late-returned-users/', TopLateReturnedUsersAPIView.as_view(), name='top-late-returned-users'),
    path('return/<int:pk>/', BookReturnAPIView.as_view(), name='book-return'),
]
