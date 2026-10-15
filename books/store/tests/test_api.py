import json

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from store.serializers import BooksSerializer
from store.models import Book


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.book_1 = Book.objects.create(name="test book 1", price=199.99, author_name="author 1")
        self.book_2 = Book.objects.create(name="test book 2", price=500.01, author_name="author 2")
        self.book_3 = Book.objects.create(name="test book 3", price=10.00, author_name="author 1")
        self.book_4 = Book.objects.create(name="test book 4", price=432.11, author_name="author 4")

    def test_get_1(self):
        url = reverse('book-list')
        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(BooksSerializer([self.book_1, self.book_2, self.book_3, self.book_4], many=True).data, response.data)

    def test_get_2(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': '4'})

        self.assertEqual(BooksSerializer(self.book_4).data, response.data[0])

    def test_get_3(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 500.01})

        self.assertEqual(BooksSerializer(self.book_2).data, response.data[0])

    def test_get_4(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price'})
        
        self.assertEqual(BooksSerializer([self.book_3, self.book_1, self.book_4, self.book_2], many=True).data, response.data)

    def test_create(self):
        url = reverse('book-list')
        data = {
            "name": "Pugs book",
            "price": "124.10",
            "author_name": "Simon"
        }
        self.client.force_login(self.user)
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(5, len(Book.objects.all()))

    def test_update(self):
        url = reverse('book-detail', args=(self.book_3.id,))
        data = {
            "price": "101.55"
        }
        self.client.force_login(self.user)
        response = self.client.patch(url, json.dumps(data), content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("101.55", response.data['price'])

    def test_delete(self):
        count_books = len(Book.objects.all())
        url = reverse('book-detail', args=(self.book_2.id,))
        self.client.force_login(self.user)

        response = self.client.delete(url)
        error_response = self.client.get(url)
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(count_books - 1, len(Book.objects.all()))
        self.assertEqual(status.HTTP_404_NOT_FOUND, error_response.status_code)