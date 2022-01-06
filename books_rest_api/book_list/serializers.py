from rest_framework import serializers

from book_list.models import BookModel


class BookSerializer(serializers.HyperlinkedModelSerializer):
    """
    class creates BookModel serializer
    """
    class Meta:
        model = BookModel
        fields = [
            'title',
            'author',
            'pub_date',
            'pub_lang',
            'isbn',
            'pages',
            'cover_link',
        ]
