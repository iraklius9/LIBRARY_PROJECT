from django.urls import path

from books import views
from books.api_views import api_return_book, api_reserve_book

app_name = 'books'

urlpatterns = [
    path('library/', views.library, name='library'),
    path('staff/', views.staff, name='staff'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),

    path('books/reserve/<int:pk>/', views.reserve_book, name='reserve_book'),
    path('mark_returned/', views.mark_returned, name='mark_returned'),
    path('api/reserve/', api_reserve_book, name='api_reserve_book'),
    path('api/return/', api_return_book, name='api_return_book'),

]
