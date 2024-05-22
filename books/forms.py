from django import forms
from books.models import BookInstance, Book
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure that the queryset filters only books with positive stock quantity
        self.fields['book'].queryset = Book.objects.filter(stock_quantity__gt=0)

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        if book and book.stock_quantity <= 0:
            raise forms.ValidationError("The selected book is not available for borrowing.")
        return cleaned_data
