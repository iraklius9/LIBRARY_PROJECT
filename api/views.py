from books.models import Author, Genre, Reservation, Book
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer, ReservationSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import datetime, timedelta


class ReservationCreateAPIView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        selected_user = request.user

        if not selected_user:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        book_id = request.data.get('book')

        existing_reservation = Reservation.objects.filter(user=selected_user, book_id=book_id).exists()

        if existing_reservation:
            return Response({'error': 'User already has a reservation for this book'},
                            status=status.HTTP_400_BAD_REQUEST)

        expires_at = datetime.now() + timedelta(hours=24)

        mutable_data = request.data.copy()

        mutable_data['user'] = selected_user.id
        mutable_data['expires_at'] = expires_at

        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookReturnAPIView(generics.UpdateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        reservation = self.get_object()
        if reservation.user == request.user:
            book = reservation.book
            book.stock_quantity += 1
            book.save()
            reservation.delete()
            return Response({'status': 'success', 'message': 'Book returned successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'You are not authorized to return this book.'},
                            status=status.HTTP_403_FORBIDDEN)


class AuthorListCreate(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]


class GenreListCreate(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]


class BookListCreate(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]


class BookRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminUser]
