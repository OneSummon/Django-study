from django.test import TestCase
from django.contrib.auth.models import User
from store.models import Book, UserBookRelation
from store.test_func import set_rating


class SetRatingTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="test user 1", first_name="fn user 1", last_name='ln user 1')
        self.user_2 = User.objects.create(username="test user 2", first_name="fn user 2", last_name='ln user 2')
        self.user_3 = User.objects.create(username="test user 3", first_name="fn user 3", last_name='ln user 3')

        self.book_1 = Book.objects.create(name="test book 1", price=199.99, author_name="author 1", owner=self.user_1)

        UserBookRelation.objects.create(user=self.user_1, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user_2, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user_3, book=self.book_1, like=True, rate=4)

    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('4.67', str(self.book_1.rating))