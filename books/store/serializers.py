from rest_framework.serializers import ModelSerializer

from .models import Book, UserBookRelation

class BooksSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class UserBookRelationSerializiter(ModelSerializer):
    class Meta:
            model = UserBookRelation
            fields = ('book', 'like', 'in_bookmarks', 'rate')