"""books_rest_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from book_list.views import (
    BookListView,
    AddBookView,
    ImportBooksView,
    BooksAPIViewSet,
    EditBookView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BookListView.as_view(), name='book_list'),
    path('add_book/', AddBookView.as_view(), name='add_book'),
    path('import/', ImportBooksView.as_view(), name='import'),
    path('books/api/', BooksAPIViewSet.as_view(), name='books_api'),
    path('edit/<int:pk>/', EditBookView.as_view(), name='edit_book'),
]
