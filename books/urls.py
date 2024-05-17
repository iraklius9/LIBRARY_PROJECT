from django.urls import path
from books.views import library_page, staff

urlpatterns = [
    path('library/', library_page, name='library'),
    path('staff/', staff, name='staff'),
]
