from django.test import TestCase
from django.db.models import Count, Case, When, Avg
from store.models import User, UserBookRelation
from store.serializers import BooksSerializer
from store.models import Book


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="test user 1")
        self.user_2 = User.objects.create(username="test user 2")
        self.user_3 = User.objects.create(username="test user 3")

    def test_ok(self):
        book_1 = Book.objects.create(name="test book 1", price=199.99, author_name="author 1")
        book_2 = Book.objects.create(name="test book 2", price=499.99, author_name="author 2")

        UserBookRelation.objects.create(user=self.user_1, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user_2, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user_3, book=book_1, like=True, rate=4)

        UserBookRelation.objects.create(user=self.user_1, book=book_2, like=True, rate=3)
        UserBookRelation.objects.create(user=self.user_2, book=book_2, like=True, rate=4)
        UserBookRelation.objects.create(user=self.user_3, book=book_2, like=False)

        books = Book.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                                            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        data = BooksSerializer(books, many=True).data
        exp_data = [
            {
                "id": book_1.id,
                "name": "test book 1",
                "price": "199.99",
                "author_name": "author 1",
                "owner": None,
                'likes_count': 3,
                'annotated_likes': 3,
                'rating': '4.67'
            },
            {
                "id": book_2.id,
                "name": "test book 2",
                "price": "499.99",
                "author_name": "author 2",
                "owner": None,
                'likes_count': 2,
                'annotated_likes': 2,
                'rating': '3.50'
            },
        ]
        self.assertEqual(exp_data, data)