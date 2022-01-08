from django.db import models


class BookModel(models.Model):
    """
    Database model storing book information
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
    """
    Database model storing isbn numbers for books
    """
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
