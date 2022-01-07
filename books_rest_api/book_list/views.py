import requests
import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from book_list.forms import (
    AddBookForm,
    ImportBooksForm,
    SearchForm,
)

from book_list.models import BookModel
from book_list.serializers import BookSerializer


class BookListView(View):
    def get(self, request):

        form = SearchForm()
        book_list = BookModel.objects.all().order_by(
            'author',
            'title',
            'pub_date',
        )
        paginator =  Paginator(book_list, 12)
        page_num = request.GET.get('page')
        books = paginator.get_page(page_num)

        return render(
            request,
            'book_list.html',
            context={
                'books': books,
                'form': form,
            }
        )

    def post(self, request):
        form = SearchForm(request.POST)

        if form.is_valid():
            search_q = form.cleaned_data['search']
            book_list = BookModel.objects.all().filter(
                Q(title__icontains=search_q) |
                Q(author__icontains=search_q) |
                Q(pub_lang__icontains=search_q)
            ).order_by(
                'author',
                'title',
                'pub_date',
            )

            if book_list:

                paginator = Paginator(book_list, 12)
                page_num = request.GET.get('page')
                books = paginator.get_page(page_num)
                form = SearchForm()

                return render(
                    request,
                    'book_list.html',
                    context={
                        'books': books,
                        'form': form,
                    }
                )
            else:
                error = 'No books found.'
                return render(
                    request,
                    'book_list.html',
                    context={
                        'form': form,
                        'error': error,
                    }
                )
        return redirect('/')


class AddBookView(View):
    def get(self, request):
        form = AddBookForm()

        return render(
            request,
            'add_book_form.html',
            context={
                'form': form,
            }
        )

    def post(self, request):
        form = AddBookForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

        else:
            return render(
                request,
                'add_book_form.html',
                context={
                    'form': form,
                }
            )

class ImportBooksView(View):
    def get(self, request):
        form = ImportBooksForm()
        return render(
            request,
            'import_books.html',
            context={
                'form': form,
            }
        )

    def post(self, request):
        form = ImportBooksForm(request.POST)
        if form.is_valid():
            query = 'https://www.googleapis.com/books/v1/volumes?q='

            search_title = form.cleaned_data['search_title']
            search_author = form.cleaned_data['search_author']
            search_isbn = form.cleaned_data['search_isbn']
            search_publisher = form.cleaned_data['search_publisher']
            search_subject = form.cleaned_data['search_subject']

            if search_title:
                query += f'+intitle:"{search_title}"'
            if search_author:
                query += f'+inauthor:"{search_author}"'
            if search_isbn:
                query += f'+isbn:{search_isbn}'
            if search_publisher:
                query += f'+inpublisher:"{search_publisher}"'
            if search_subject:
                query += f'+subject:"{search_subject}"'

            resp = requests.get(query)
            if resp.status_code == 200:
                books = json.loads(resp.text)
            else:
                books = Nonepip

            if books:
                for b in books['items']:
                    book = BookModel.objects.create(title=b['volumeInfo']['title'])

                    if 'authors' in b['volumeInfo']:
                        book.author = ', '.join(b['volumeInfo']['authors'])

                    if 'publishedDate' in b['volumeInfo']:
                        book.pub_date = b['volumeInfo']['publishedDate']

                    if 'language' in b['volumeInfo']:
                        book.pub_lang = b['volumeInfo']['language']

                    if 'industryIdentifiers' in b['volumeInfo']:
                        for element in b['volumeInfo']['industryIdentifiers']:
                            if 'isbn' in element['type'].lower():
                                book.isbn += f"{element['type']}: {element['identifier']} "

                    if 'pageCount' in b['volumeInfo']:
                        book.pages = int(b['volumeInfo']['pageCount'])

                    if 'imageLinks' in b['volumeInfo']:
                        book.cover_link = b['volumeInfo']['imageLinks']['thumbnail']

                    book.save()

                books_added = f"Books imported: {len(books['items'])}"

                return render(
                    request,
                    'import_books.html',
                    context={
                        "conf_msg": books_added,
                        "form": form,
                    }
                )

            return render(
                request,
                'import_books.html',
                context={
                    'form': form,
                    'conf_msg': 'No books found',
                }
            )


class BookViewSet(viewsets.ModelViewSet):
    """
    API end point allowing to view book list.
    Pagination set to 10 entries per page.
    """
    queryset = BookModel.objects.order_by('title', 'author', 'pub_date')
    serializer_class = BookSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    # Set up filtering options.
    # filterset_fields = ['title', 'author', 'pub_lang']
    # use search instead of filtering.
    search_fields = ['title', 'author', 'pub_lang']
    ordering_fields = ['title', 'author', 'pub_lang']
    ordering = ['title', 'author', 'pub_date']
