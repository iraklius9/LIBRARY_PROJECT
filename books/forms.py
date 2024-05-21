from django import forms


class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search by title', required=False)
    author = forms.CharField(label='Search by author', required=False)
    genre = forms.CharField(label='Search by genre', required=False)
