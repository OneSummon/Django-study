from django.db.models import Avg, When, Case, Count
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsOwnerOrStaffOrReadOnly
from django.shortcuts import render

from .models import Book, UserBookRelation
from .serializers import BooksSerializer, UserBookRelationSerializiter

# Create your views here.
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                                           rating=Avg('userbookrelation__rate')).order_by('id')
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filterset_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_fields = ['price']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserBookRelationView(UpdateModelMixin,GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializiter
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user, book_id=self.kwargs['book'])
        return obj

def auth(request):
    return render(request, 'oauth.html')