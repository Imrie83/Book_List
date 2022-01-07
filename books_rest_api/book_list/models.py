from django.core.exceptions import ValidationError
from django.db import models


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


class BookModel(models.Model):
    """
    class creates database model storing book information
    """

    title = models.CharField(
        max_length=255,
        verbose_name='Title',
        null=False,
    )
    author = models.CharField(
        max_length=255,
        verbose_name='Author',
        null=True,
    )
    pub_date = models.CharField(
        max_length=10,
        verbose_name='Publication date',
        null=True,
    )
    pub_lang = models.CharField(
        max_length=255,
        verbose_name='Publication language',
        null=True,
    )
    pages = models.IntegerField(
        verbose_name='Number of pages',
        null=True,
    )
    cover_link = models.URLField(
        max_length=255,
        verbose_name='Cover link',
        null=True,
    )


class IsbnModel(models.Model):
    isbn_type = models.CharField(
        max_length=255,
        verbose_name='type',
        null=True,
    )
    isbn_num = models.CharField(
        max_length=255,
        verbose_name='isbn',
        null=True,
    )
    book = models.ForeignKey(
        to=BookModel,
        related_name='book_isbn',
        on_delete=models.CASCADE,
    )
