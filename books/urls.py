from django.conf.urls.static import static
from django.urls import path

from LIBRARY_PROJECT import settings
from books.views import staff, library, book_detail

urlpatterns = [
    path('library/', library, name='library'),
    path('staff/', staff, name='staff'),
    path('book/<int:book_id>/', book_detail, name='book_detail')

]

