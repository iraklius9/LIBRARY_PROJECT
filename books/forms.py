from django import forms
from books.models import BookInstance, Book, BorrowingHistory, Reservation
from users.models import CustomUser


class BorrowForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        widget=forms.Select(attrs={'class': 'searchable'})
    )
    borrower = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.Select(attrs={'class': 'searchable'})
    )

    class Meta:
        model = BookInstance
        fields = ['book', 'borrower', 'borrowed_date', 'returned_date', 'status']
        widgets = {
            'borrowed_date': forms.DateInput(attrs={'type': 'date'}),
            'returned_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        if book and book.stock_quantity <= 0:
            user = cleaned_data.get('borrower')
            user_reservation = Reservation.objects.filter(book=book, user=user).exists()
            if not user_reservation:
                raise forms.ValidationError("The selected book is not available for borrowing.")
        return cleaned_data


class ReturnBookForm(forms.Form):
    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        widget=forms.Select(attrs={'class': 'searchable'})
    )
    borrower = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.Select(attrs={'class': 'searchable'})
    )
    returning_date = forms.DateField(label='Returning Date', required=False,
                                     widget=forms.DateInput(attrs={'type': 'date'}))


class BorrowingHistoryAdminForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        widget=forms.Select(attrs={'class': 'searchable'})
    )

    class Meta:
        model = BorrowingHistory
        fields = ['book', 'borrower', 'returning_date', 'borrowing_date']
        widgets = {
            'borrowing_date': forms.DateInput(attrs={'type': 'date'}),
            'returning_date': forms.DateInput(attrs={'type': 'date'}),
        }
