from rest_framework.serializers import ModelSerializer, SerializerMethodField, DecimalField

from .models import Book, UserBookRelation

class BooksSerializer(ModelSerializer):
    annotated_likes = SerializerMethodField()
    rating = DecimalField(max_digits=3, decimal_places=2, read_only=True, default=None)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name', 'owner', 'annotated_likes', 'rating')

    # def get_likes_count(self, instance):
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()

    def get_annotated_likes(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()

class UserBookRelationSerializiter(ModelSerializer):
    class Meta:
            model = UserBookRelation
            fields = ('book', 'like', 'in_bookmarks', 'rate')