from django.contrib.auth import get_user_model
from django.db.models import Count, F, Q
from datetime import datetime, timedelta
from django.utils import timezone
from books.models import Author, Genre, Reservation, Book, BookInstance
from api.serializers import BookSerializer, AuthorSerializer, GenreSerializer, ReservationSerializer, \
    BookInstanceSerializer, BookInstanceSerializer2, ReservationSerializer2
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.models import CustomUser


class ReservationCreateAPIView(generics.CreateAPIView):
    serializer_class = ReservationSerializer2
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')

        existing_reservation = Reservation.objects.filter(user=request.user, book_id=book_id).exists()
        if existing_reservation:
            return Response({'error': 'User already has a reservation for this book'},
                            status=status.HTTP_400_BAD_REQUEST)

        mutable_data = request.data.copy()
        mutable_data['user'] = request.user.id

        mutable_data['expires_at'] = timezone.now() + timedelta(hours=24)

        serializer = self.get_serializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationCheckAPIView(generics.GenericAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        borrower_data = request.data.get('user')

        if not borrower_data:
            return Response({'status': 'error', 'message': 'Borrower data is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()

        try:
            borrower = User.objects.get(**{'id': borrower_data})
            reservations = Reservation.objects.filter(user=borrower)
            if reservations.exists():
                serializer = self.serializer_class(reservations, many=True)
                return Response({'status': 'success', 'message': 'Reservations found.', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'No reservations found for the borrower'},
                                status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'Borrower not found'}, status=status.HTTP_404_NOT_FOUND)


class BookReturnAPIView(generics.UpdateAPIView):
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer2
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        book_instance = self.get_object()

        if book_instance.status == 'On loan':
            borrower_id = request.data.get('borrower', None)
            if borrower_id:
                try:
                    borrower = CustomUser.objects.get(pk=borrower_id)
                    book_instance.status = 'Returned'
                    book_instance.borrower = borrower
                    book_instance.returned_date = timezone.now()
                    book_instance.save()

                    book_instance.book.stock_quantity += 1
                    book_instance.book.save()
                    return Response({'status': 'success', 'message': 'Book returned successfully.'},
                                    status=status.HTTP_200_OK)
                except CustomUser.DoesNotExist:
                    return Response({'status': 'error', 'message': 'Borrower not found.'},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'status': 'error', 'message': 'Please provide a borrower.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'error', 'message': 'Book is not on loan.'}, status=status.HTTP_400_BAD_REQUEST)


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


class MostPopularBooksAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.annotate(num_borrowed=Count('borrowinghistory')).order_by('-num_borrowed')[:10]


class BooksBorrowedLastYearAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        last_year = datetime.now() - timedelta(days=365)
        return Book.objects.annotate(
            num_borrowed_this_year=Count(
                'borrowinghistory',
                filter=Q(borrowinghistory__borrowing_date__gte=last_year)
            )
        ).order_by('-num_borrowed_this_year')


class TopLateReturnedBooksAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.annotate(
            num_late_returns=Count('borrowinghistory', filter=Q(
                borrowinghistory__returning_date__gt=F('borrowinghistory__book_instance__returned_date')))
        ).order_by('-num_late_returns')[:100]


class TopLateReturnedUsersAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookInstanceSerializer

    def get_queryset(self):
        CustomUser = get_user_model()

        user_late_return_counts = CustomUser.objects.annotate(
            num_late_returns=Count('bookinstance',
                                   filter=Q(bookinstance__returned_date__gt=F('bookinstance__borrowed_date')))
        ).order_by('-num_late_returns')[:100]

        return user_late_return_counts.values('id', 'username', 'num_late_returns')
