from django.contrib import admin

from .models import Author
from .models import Tag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ['name', 'email']
    ordering = ['name']
    search_fields = [
        'name', 'email', 'short_description', 'long_description']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ['name', 'description']
    ordering = ['name']
    search_fields = ['name', 'description']
