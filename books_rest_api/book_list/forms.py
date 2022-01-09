from django import forms
from django.core.exceptions import ValidationError
from book_list.models import BookModel


def validate_isbn(isbn):
    """
    function validates isbn number
    :param isbn:
    :raise: ValidationError
    """

    i = 1
    control = 0

    if '-' in isbn:
        temp_list = isbn.split('-')
        isbn = ''.join(temp_list)

    for digit in isbn[:-1]:
        if not digit.isdigit():
            raise ValidationError('ISBN must consist of numbers.')

    if isbn[-1] == 'X':
        check_sum = 10
    else:
        check_sum = int(isbn[-1])

    if len(isbn) == 10:
        for num in isbn[:-1]:
            control += int(num) * i
            i += 1
        control = control % 11

        if not control == check_sum:
            raise ValidationError(f'{isbn} is not a valid isbn')

    elif len(isbn) == 13:
        for num in isbn[:-1:2]:
            control += int(num)
        for num in isbn[1:-1:2]:
            control += int(num) * 3

        if control % 10 == 0:
            control = 0
        else:
            control = 10 - (control % 10)

        if not control == check_sum:
            raise ValidationError(f'{isbn} is not a valid isbn')

    else:
        raise ValidationError(f'{isbn} is not a valid isbn')


class DatePickerField(forms.DateInput):
    """
    Create a date-input field
    """
    input_type = 'date'


class AddBookForm(forms.ModelForm):
    """
    Create a form allowing to manually add a book to db
    """
    class Meta:
        model = BookModel
        fields = '__all__'

        labels = {
            'title': '',
            'author': '',
            'pub_date': 'Published on',
            'pub_lang': '',
            'pages': '',
            'cover_link': '',
        }

        widgets = {
            'pub_date': DatePickerField(),
        }

    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'placeholder': 'Title',
            'aria-label': 'book title',
        })
        self.fields['author'].widget.attrs.update({
            'placeholder': 'Author',
            'aria-label': 'author',
        })
        self.fields['pub_lang'].widget.attrs.update({
            'placeholder': 'Publication language',
            'aria-label': 'publication language',
        })
        self.fields['pages'].widget.attrs.update({
            'placeholder': 'Number of pages',
            'aria-label': 'number of pages',
        })
        self.fields['cover_link'].widget.attrs.update({
            'placeholder': 'Link to book cover',
            'aria-label': 'link to book cover',
        })
        self.fields['pub_date'].widget.attrs.update({
            'class': 'pick-date',
            'aria-label': 'publication date',
        })
        self.fields['author'].required = False
        self.fields['pub_lang'].required = False
        self.fields['pub_date'].required = False
        self.fields['pages'].required = False
        self.fields['cover_link'].required = False


class ImportBooksForm(forms.Form):
    """
    Create a form allowing to import books from Google Books API
    """
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

    search_title.widget.attrs.update({
        'placeholder': 'title',
        'aria-label': 'search by title',
    })
    search_author.widget.attrs.update({
        'placeholder': 'author',
        'aria-label': 'search by author',
    })
    search_isbn.widget.attrs.update({
        'placeholder': 'isbn',
        'aria-label': 'search by isbn',
    })
    search_subject.widget.attrs.update({
        'placeholder': 'category',
        'aria-label': 'search by category',
    })
    search_publisher.widget.attrs.update({
        'placeholder': 'publisher',
        'aria-label': 'search by publisher',
    })


class SearchForm(forms.Form):
    """
    Form allowing to search book list by keywords and date range.
    """
    search = forms.CharField(
        max_length=255,
        required=False,
        label='Search',
    )
    date_from = forms.CharField(
        max_length=255,
        required=False,
        label='Publication span',
        widget=DatePickerField(attrs={
            'aria-label': 'published after',
        })
    )
    date_to = forms.CharField(
        max_length=255,
        required=False,
        label='',
        widget=DatePickerField(attrs={
            'aria-label': 'published before',
        })

    )

    search.widget.attrs.update({
        'placeholder': 'title / author / language',
        'class': 'search-bar',
        'aria-label': 'search keyword',
    })
    date_from.widget.attrs.update({
        'class': 'date-picker',
        'aria-label': 'search after publication date',
    })
    date_to.widget.attrs.update({
        'class': 'date-picker',
        'aria-label': 'search before publication date',
    })


class AddISBNForm(forms.Form):
    """
    Form allowing to add books isbn when adding book manually.
    """
    isbn_num = forms.CharField(
        max_length=20,
        required=False,
        label='',
        validators=[validate_isbn],
    )

    isbn_num.widget.attrs.update({
        'placeholder': 'ISBN number',
        'aria-label': 'add isbn',
    })
