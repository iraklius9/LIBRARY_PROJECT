from django.urls import path

from books import views

app_name = 'books'

urlpatterns = [
    path('library/', views.library, name='library'),
    path('staff/', views.staff, name='staff'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/return/', views.return_book, name='return_book'),
    path('books/reserve/<int:pk>/', views.reserve_book, name='reserve_book'),
    path('book/<int:pk>/cancel_reservation/', views.cancel_reservation, name='cancel_reservation'),
    path('staff/reservations/', views.check_reservations, name='check_reservations'),

]
