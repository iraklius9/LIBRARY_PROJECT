from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from books.models import Book, Author, Genre, Reservation, BookInstance


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    num_borrowed_this_year = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_date', 'stock_quantity', 'image', 'author', 'genre',
                  'num_borrowed_this_year']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['book', 'expires_at']

    def create(self, validated_data):

        request = self.context.get("request")
        expires_at = timezone.now() + timedelta(hours=24)
        validated_data["user"] = request.user
        validated_data["expires_at"] = expires_at
        return super().create(validated_data)


class BookInstanceSerializer(serializers.ModelSerializer):
    borrower_email = serializers.EmailField(source='borrower.email', read_only=True)

    class Meta:
        model = BookInstance
        fields = ['id', 'borrower_email']


class BookInstanceSerializer2(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = ['borrower', 'book']
        read_only_fields = ['book']


class ReservationSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['expires_at']

    def create(self, validated_data):
        """
        Create and return a new Reservation instance.
        """
        request = self.context.get("request")
        expires_at = timezone.now() + timedelta(hours=24)
        validated_data["user"] = request.user
        validated_data["expires_at"] = expires_at
        return super().create(validated_data)
