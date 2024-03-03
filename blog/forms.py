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
    title = forms.CharField(max_length=255)
    thumbnail = forms.CharField(max_length=1024)
    body = forms.CharField(required=False,
                           widget=CKEditorWidget())
    # tags = forms.CharField(max_length=255)

    class Meta:
        model = Post
        fields = ['title',  'thumbnail', 'body', 'tags']

    def __init__(self, *args, **kwargs):
        # Call to ModelForm constructor
        super(AddPostForm, self).__init__(*args, **kwargs)
        self.fields['thumbnail'].widget.attrs['style'] = 'width:700px;'
        self.fields['thumbnail'].widget.attrs['placeholder'] = 'image url'
        self.fields['title'].widget.attrs['style'] = 'width:700px;'
        self.fields['title'].widget.attrs['placeholder'] = 'interesting blog title'
        self.fields['tags'].widget.attrs['placeholder'] = 'comma separated list of tags'
        self.fields['tags'].widget.attrs['style'] = 'width:350px;'
