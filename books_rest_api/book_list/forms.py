from django import forms
from book_list.models import BookModel


class DatePickerField(forms.DateInput):
    """
    Create a date-input field
    """
    input_type = 'date'


class AddBookForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = '__all__'
        widgets = {
            'pub_date': DatePickerField(),
        }


class ImportBooksForm(forms.Form):
    search_title = forms.CharField(
        max_length=255,
        label='',
        required=False,
    )
    search_author = forms.CharField(
        max_length=255,
        label='',
        required=False,
    )
    search_isbn = forms.CharField(
        max_length=255,
        label='',
        required=False,
    )
    search_subject = forms.CharField(
        max_length=255,
        label='',
        required=False,
    )
    search_publisher = forms.CharField(
        max_length=255,
        label='',
        required=False,
    )

    search_title.widget.attrs.update({'placeholder': 'title'})
    search_author.widget.attrs.update({'placeholder': 'author'})
    search_isbn.widget.attrs.update({'placeholder': 'isbn'})
    search_subject.widget.attrs.update({'placeholder': 'category'})
    search_publisher.widget.attrs.update({'placeholder': 'publisher'})
