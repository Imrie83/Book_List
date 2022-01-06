from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from book_list.forms import AddBookForm
from book_list.models import BookModel


class BookListView(View):
    def get(self, request):
        books = BookModel.objects.all().order_by(
            'author',
            'title',
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
