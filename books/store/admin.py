from django.contrib import admin
from .models import Book, UserBookRelation

# Register your models here.

admin.site.register(Book)
admin.site.register(UserBookRelation)