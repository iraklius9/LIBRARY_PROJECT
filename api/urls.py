from django.urls import path
from .views import AuthorListCreate, GenreListCreate, BookListCreate, BookRetrieveUpdateDestroy

urlpatterns = [
    path('authors/', AuthorListCreate.as_view(), name='author-list-create'),
    path('genres/', GenreListCreate.as_view(), name='genre-list-create'),
    path('books/', BookListCreate.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroy.as_view(), name='book-retrieve-update-destroy'),
]
