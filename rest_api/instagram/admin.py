from .models import Post
from django.contrib import admin


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['message']
    list_display = ['pk', 'message', 'author']