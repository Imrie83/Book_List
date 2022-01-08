import pytest
from book_list.models import (
    BookModel,
    IsbnModel,
)


@pytest.fixture
def example_books():
    """
    create example books required for testing
    :return: list of example books
    """
    book1 = BookModel.objects.create(
        title='Warriors of God',
        author='Andrzej Sapkowski',
        pub_date='2021-10-19',
        pub_lang='pl',
        pages=672,
    )
    book2 = BookModel.objects.create(
        title='Mitologia Słowiańska',
        author='Jakub Bobrowski',
        pub_date='2017',
        pub_lang='pl',
        pages=160,
    )
    book3 = BookModel.objects.create(
        title='Titanicus',
        author='Dan Abnett',
        pub_date='2018-07-26',
        pub_lang='en',
        pages=512,
    )
    return [book1, book2, book3]


@pytest.fixture
def isbn_number(example_books):
    """
    Create isbn numbers corresponding to books in db.
    :param example_books:
    """
    isbn1 = IsbnModel.objects.create(
        isbn_num='9780316423724',
        isbn_type='ISBN_13',
        book=example_books[0],
    )
    isbn2 = IsbnModel.objects.create(
        isbn_num='0316423726',
        isbn_type='ISBN_10',
        book=example_books[0],
    )
    isbn3 = IsbnModel.objects.create(
        isbn_num='9788375763256',
        book=example_books[1],
        isbn_type='ISBN_13',
    )
    isbn4 = IsbnModel.objects.create(
        isbn_num='837576325X',
        book=example_books[1],
        isbn_type='ISBN_10',
    )
    isbn4 = IsbnModel.objects.create(
        isbn_num='9781784968168',
        book=example_books[2],
        isbn_type='ISBN_13',
    )
