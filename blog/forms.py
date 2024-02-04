from django import forms
from .models import Comment, Post
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class AddPostForm(forms.ModelForm):
    # title = forms.CharField(max_length=255)
    # thumbnail = forms.CharField(max_length=1024)
    body = forms.CharField(required=False,
                           widget=CKEditorWidget())
    # tags = forms.CharField(max_length=255)

    class Meta:
        model = Post
        fields = ['title',  'thumbnail', 'body', 'tags']
