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
