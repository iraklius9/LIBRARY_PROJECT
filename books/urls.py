from django.urls import path
from books.views import library_page

urlpatterns = [
    path('library/', library_page, name='library'),
]
