from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        field = [
            'messge', 'photo', 'tag_set', 'is_public'
        ]
        # exclude = []