from rest_framework import serializers

from book_list.models import BookModel, IsbnModel


class IsbnSerializer(serializers.ModelSerializer):
    """
    Create ISBN model serializer.
    """
    class Meta:
        model = IsbnModel
        fields = [
            'isbn_type',
            'isbn_num',
        ]


class BookSerializer(serializers.ModelSerializer):
    """
    Create BookModel serializer with nested ISBN serialiser.
    """
    isbn = IsbnSerializer(
        many=True,
        read_only=True,
        source='book_isbn',
    )

    class Meta:
        model = BookModel
        fields = [
            'title',
            'author',
            'pub_date',
            'pub_lang',
            'pages',
            'isbn',
            'cover_link',
        ]
