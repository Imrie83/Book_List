import requests
import json
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from book_list.forms import (
    AddBookForm,
    ImportBooksForm,
    SearchForm, AddISBNForm,
)

from book_list.models import BookModel, IsbnModel
from book_list.serializers import BookSerializer


class BookListView(View):
    """
    Class creates a view listing all books from db.

    Get method returns a list of all books with pagination (set to 12 per page)
    and form in context.

    Post method allows searching books in database based on keywords as well as
    date range. If no books found returns form, error message and books
    available, if books matching query found returns paginated
    queryset with form.
    """

    def get(self, request):
        form = SearchForm()
        book_list = BookModel.objects.all().order_by(
            'author',
            'title',
            'pub_date',
        )
        paginator = Paginator(book_list, 12)
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

            if form.cleaned_data['date_from']:
                book_list = book_list.filter(
                    pub_date__gte=form.cleaned_data['date_from']
                )

            if form.cleaned_data['date_to']:
                book_list = book_list.filter(
                    pub_date__lte=form.cleaned_data['date_to']
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
                error = 'No books found'
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
    """
    Class creates a view allowing to add books to database.

    Get method pass forms in context and display template.

    Post method validates data from forms - if data correct, save it to db and
    redirect to book list, if data incorrect returns form with appropriate
    error / validation messages for user.
    """

    def get(self, request):
        form = AddBookForm()
        isbn_form = AddISBNForm()

        return render(
            request,
            'add_book_form.html',
            context={
                'form': form,
                'isbn_form': isbn_form,
            }
        )

    def post(self, request):

        form = AddBookForm(request.POST)
        isbn_form = AddISBNForm(request.POST)

        if form.is_valid() and isbn_form.is_valid():
            book = form.save()

            if isbn_form.cleaned_data['isbn_num']:
                isbn_type = ''
                if len(isbn_form.cleaned_data['isbn_num']) == 10:
                    isbn_type = 'ISBN_10'
                elif len(isbn_form.cleaned_data['isbn_num']) == 13:
                    isbn_type = 'ISBN_13'

                IsbnModel.objects.create(
                    book_id=book.pk,
                    isbn_type=isbn_type,
                    isbn_num=isbn_form.cleaned_data['isbn_num']
                )

            return redirect('/')

        else:
            return render(
                request,
                'add_book_form.html',
                context={
                    'form': form,
                    'isbn_form': isbn_form,
                }
            )


class ImportBooksView(View):
    """
    Class creates a view allowing to import books from Google Books API

    Get method display import form.

    Post method gets data from import form, builds import query and uses it
    to retrieve data from Google Books API. After receiving data from
    Google Books API tries to save the data in database and returns to book
    list with information about number of imported books. If no books
    matching query found, returns to form with appropriate message
    """

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
            max_result = 40
            query = 'https://www.googleapis.com/books/v1/volumes?q='

            search_title = form.cleaned_data['search_title']
            search_author = form.cleaned_data['search_author']
            search_isbn = form.cleaned_data['search_isbn']
            search_publisher = form.cleaned_data['search_publisher']
            search_subject = form.cleaned_data['search_subject']

            # build query with import criteria
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
            query += f'&maxResults={max_result}&startIndex='  # max allowed results

            # query start index
            start_index = '0'
            resp = requests.get(query + start_index)

            # if any books found
            if resp.status_code == 200 and json.loads(resp.text)['totalItems']:
                books = json.loads(resp.text)['items']
                books_num = int(json.loads(resp.text)['totalItems'])

                # perform multiple queries if number of books found
                # is greater than max allowed per query (40) and add
                # query results to book list.
                while books_num >= 41:
                    start_index = str(int(start_index) + 40)
                    books_num -= 40
                    resp = requests.get(query + start_index)
                    books += json.loads(resp.text)['items']
            else:
                books = None

            if books:
                # debug...
                print(f'books found: {len(books)}')

                books_added = 0
                for b in books:
                    try:
                        title = b['volumeInfo']['title']
                    except KeyError as e:
                        print(e)
                        title = None

                    try:
                        author = ', '.join(b['volumeInfo']['authors'])
                    except KeyError as e:
                        print(e)
                        author = None

                    try:
                        pub_date = b['volumeInfo']['publishedDate']
                    except KeyError as e:
                        print(e)
                        pub_date = None

                    try:
                        pub_lang = b['volumeInfo']['language']
                    except KeyError as e:
                        print(e)
                        pub_lang = None

                    try:
                        page_count = int(b['volumeInfo']['pageCount'])
                    except KeyError as e:
                        print(e)
                        page_count = None

                    try:
                        isbn = b['volumeInfo']['industryIdentifiers']
                    except KeyError as e:
                        print(e)
                        isbn = None

                    try:
                        cover_link = b['volumeInfo']['imageLinks']['thumbnail']
                    except KeyError as e:
                        print(e)
                        cover_link = None

                    if title:
                        if not BookModel.objects.filter(
                                title=title,
                                author=author,
                                pub_lang=pub_lang,
                                pub_date=pub_date,
                        ).exists():
                            book = BookModel.objects.create(
                                title=title,
                                author=author,
                                pub_date=pub_date,
                                pub_lang=pub_lang,
                                pages=page_count,
                                cover_link=cover_link,
                            )
                            books_added += 1
                            if isbn:
                                for num in isbn:
                                    if 'isbn' in num['type'].lower():
                                        IsbnModel.objects.create(
                                            book_id=book.pk,
                                            isbn_num=num['identifier'],
                                            isbn_type=num['type'],
                                        )
                # if 'title' in b['volumeInfo']:
                    #     book = BookModel.objects.create(
                    #         title=b['volumeInfo']['title']
                    #     )
                    #     books_added += 1
                    #
                    #     if 'authors' in b['volumeInfo']:
                    #         book.author = ', '.join(b['volumeInfo']['authors'])
                    #
                    #     if 'publishedDate' in b['volumeInfo']:
                    #         book.pub_date = b['volumeInfo']['publishedDate']
                    #
                    #     if 'language' in b['volumeInfo']:
                    #         book.pub_lang = b['volumeInfo']['language']
                    #
                    #     if 'pageCount' in b['volumeInfo']:
                    #         book.pages = int(b['volumeInfo']['pageCount'])
                    #
                    #     if 'imageLinks' in b['volumeInfo']:
                    #         book.cover_link = (
                    #             b['volumeInfo']['imageLinks']['thumbnail']
                    #         )
                    #
                    #     book.save()
                    #
                    #     if 'industryIdentifiers' in b['volumeInfo']:
                    #         for element in (
                    #                 b['volumeInfo']['industryIdentifiers']
                    #         ):
                    #             if 'isbn' in element['type'].lower():
                    #                 IsbnModel.objects.create(
                    #                     book_id=book.pk,
                    #                     isbn_num=element['identifier'],
                    #                     isbn_type=element['type'],
                    #                 )

                form = ImportBooksForm()
                return render(
                    request,
                    'import_books.html',
                    context={
                        "conf_msg": f'Books imported: {books_added}',
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


class BooksAPIViewSet(generics.ListAPIView):
    """
    API end point allowing to view book list.
    Pagination set to 10 entries per page.
    """
    queryset = BookModel.objects.order_by('title', 'author', 'pub_date')
    serializer_class = BookSerializer
    model = BookModel
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
