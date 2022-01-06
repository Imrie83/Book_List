import requests
import json
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from book_list.forms import AddBookForm, ImportBooksForm
from book_list.models import BookModel


class BookListView(View):
    def get(self, request):
        books = BookModel.objects.all().order_by(
            'author',
            'title',
            'pub_date',
        )

        return render(
            request,
            'book_list.html',
            context={
                'books': books,
            }
        )


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
                books = None

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
