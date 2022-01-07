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
        self.fields['title'].widget.attrs.update({'placeholder': 'Title'})
        self.fields['author'].widget.attrs.update({'placeholder': 'Author'})
        self.fields['pub_lang'].widget.attrs.update({
            'placeholder': 'Publication language'
        })
        self.fields['pages'].widget.attrs.update({'placeholder': 'Number of pages'})
        self.fields['cover_link'].widget.attrs.update({
            'placeholder': 'Link to book cover'
        })
        self.fields['author'].required = False
        self.fields['pub_lang'].required = False
        self.fields['pub_date'].required = False
        self.fields['pages'].required = False
        self.fields['cover_link'].required = False


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
