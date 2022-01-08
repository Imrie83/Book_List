import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.urls import resolve, reverse

from book_list.models import BookModel, IsbnModel
from book_list.views import (
    BookListView,
    AddBookView,
    ImportBooksView,
    BookViewSet,
)


def test_urls():
    """
    Test urls.
    """
    # main page / book list
    found = resolve(reverse('book_list'))
    assert found.func.view_class == BookListView

    # manual book addition page
    found = resolve(reverse('add_book'))
    assert found.func.view_class == AddBookView

    # import from Google Books page
    found = resolve(reverse('import'))
    assert found.func.view_class == ImportBooksView

    # rest api view
    found = resolve(reverse('books_api'))
    assert found.func.view_class == BookViewSet


@pytest.mark.django_db
def test_database(client, example_books):
    """
    test if book model works correctly
    :param client:
    :param example_books:
    """
    books = BookModel.objects.all()
    assert len(books) == 3

    try:
        test_book = BookModel.objects.get(title='Titanicus')
        assert 'Dan Abnett' in test_book.author
        assert test_book.pages == 512
        test_book.delete()
        books = BookModel.objects.all()
        assert len(books) == 2
    except ObjectDoesNotExist as e:
        print(e)


@pytest.mark.django_db
def test_book_list(client, example_books):
    """
    Test loading main page and extracting books to display from db
    :param client:
    :param example_books:
    """
    response = client.get('/')
    assert response.status_code == 200
    assert len(response.context['books']) == 3
    assert example_books[0] in response.context['books']
    assert example_books[1] in response.context['books']
    assert example_books[2] in response.context['books']


@pytest.mark.django_db
def test_book_search_by_keyword(client, example_books):
    """
    Test book search by keyword
    :param client:
    :param example_books:
    """
    response = client.post('/',
                           {
                               'search': 'Titanicus',
                           })
    assert response.status_code == 200
    assert len(response.context['books']) == 1
    assert response.context['books'][0].author == 'Dan Abnett'


@pytest.mark.django_db
def test_book_search_by_date_from(client, example_books):
    """
    Test book search by "date from" value
    :param client:
    :param example_books:
    """
    response = client.post('/',
                           {
                               'date_from': '2018',
                           })

    assert response.status_code == 200
    assert len(response.context['books']) == 2
    assert response.context['books'][0].author == 'Andrzej Sapkowski'
    assert response.context['books'][1].author == 'Dan Abnett'


@pytest.mark.django_db
def test_book_search_by_date_to(client, example_books):
    """
    Test book search by "date to" value
    :param client:
    :param example_books:
    """
    response = client.post('/',
                           {
                               'date_to': '2017',
                           })

    assert response.status_code == 200
    assert len(response.context['books']) == 1
    assert response.context['books'][0].author == 'Jakub Bobrowski'


@pytest.mark.django_db
def test_book_search_by_date_range(client, example_books):
    """
    Test book search by date range
    :param client:
    :param example_books:
    """
    response = client.post('/',
                           {
                               'date_from': '2018',
                               'date_to': '2019',
                           })

    assert response.status_code == 200
    assert len(response.context['books']) == 1
    assert response.context['books'][0].author == 'Dan Abnett'


@pytest.mark.django_db
def test_manual_add_book(client):
    """
    Test if book created correctly
    :param client:
    """
    assert len(BookModel.objects.all()) == 0
    assert len(IsbnModel.objects.all()) == 0

    response = client.post('/add_book/',
                           {
                            'title': 'Some Test Book',
                            'author': 'Dan Abnett',
                            'pub_date': '2011-11-11',
                            'pub_lan': 'en',
                            'pages': '696',
                            'isbn_num': '9780316423724',
                           })

    assert response.status_code == 302
    assert BookModel.objects.all().count() == 1
    assert BookModel.objects.last().title == 'Some Test Book'

    assert IsbnModel.objects.last().isbn_type == 'ISBN_13'
    assert IsbnModel.objects.last().isbn_num == '9780316423724'


@pytest.mark.django_db
def test_book_api_import(client):
    """
    test importing books from Google Books API
    :param client:
    """
    assert len(BookModel.objects.all()) == 0
    response = client.post('/import/',
                           {
                               'search_isbn': '837576325X'
                           })

    assert response.status_code == 200
    assert response.context['conf_msg'] == 'Books imported: 1'
    assert len(BookModel.objects.all()) == 1
    assert BookModel.objects.last().author == 'Jakub Bobrowski'
