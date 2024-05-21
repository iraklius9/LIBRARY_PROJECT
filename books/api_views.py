# books/api_views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Book, Reservation
from .serializers import ReservationSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_reserve_book(request):
    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
        reservation = serializer.save(user=request.user, expires_at=timezone.now() + timedelta(days=1))
        return Response({'status': 'success', 'message': 'Book reserved successfully.'})
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_return_book(request):
    book_id = request.data.get('book_id')
    user_id = request.data.get('user_id')
    try:
        reservation = Reservation.objects.get(book_id=book_id, user_id=user_id)
        reservation.delete()
        return Response({'status': 'success', 'message': 'Book returned successfully.'})
    except Reservation.DoesNotExist:
        return Response({'status': 'error', 'message': 'Reservation not found.'}, status=404)
