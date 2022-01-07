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

    check_sum = isbn[-1]

    if check_sum == 'X':
        check_sum = 10
    else:
        check_sum = int(check_sum)

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
    class Meta:
        model = BookModel
        fields = '__all__'

        labels = {
            'title': '',
            'author': '',
            'pub_date': 'Published on',
            'pub_lang': '',
            'isbn': '',
            'pages': '',
            'cover_link': '',
        }

        widgets = {
            'pub_date': DatePickerField(),
        }

    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Title'})
        self.fields['author'].widget.attrs.update({'placeholder': 'Author'})
        self.fields['pub_lang'].widget.attrs.update({
            'placeholder': 'Publication language'
        })
        self.fields['isbn'].widget.attrs.update({'placeholder': 'ISBN'})
        self.fields['pages'].widget.attrs.update({'placeholder': 'Number of pages'})
        self.fields['cover_link'].widget.attrs.update({
            'placeholder': 'Link to book cover'
        })


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


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label='Search',
    )
    date_from = forms.CharField(
        max_length=255,
        required=False,
        label='Publication span',
        widget=DatePickerField()
    )
    date_to = forms.CharField(
        max_length=255,
        required=False,
        label='',
        widget=DatePickerField()

    )

    search.widget.attrs.update({
        'placeholder': 'title / author / language',
        'class': 'search-bar'
    })
    date_from.widget.attrs.update({
        'class': 'date-picker'
    })
    date_to.widget.attrs.update({
        'class': 'date-picker'
    })


class AddISBNForm(forms.Form):

    isbn_num = forms.CharField(
        max_length=20,
        required=False,
        label='',
        validators=[validate_isbn],
    )

    isbn_num.widget.attrs.update({
        'placeholder': 'ISBN number'
    })

