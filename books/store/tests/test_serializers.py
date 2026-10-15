from django.test import TestCase

from store.serializers import BooksSerializer
from store.models import Book


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book = Book.objects.create(name="test book", price=199.99, author_name="author")
        data = BooksSerializer(book).data

        exp_data = {
            "id": book.id,
            "name": "test book",
            "price": "199.99",
            "author_name": "author"
        }
        self.assertEqual(exp_data, data)