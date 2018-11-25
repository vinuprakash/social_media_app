from django import forms
from . import models

class PostForm(forms.ModelForm):

    class Meta:
        model = models.Post
        fields = ['title','content']

        widgets = {
            'content': forms.Textarea(attrs={'class':'editable'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = ['content']
