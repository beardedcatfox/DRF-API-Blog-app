from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Author, Post


class AuthorRegisterForm(UserCreationForm):

    class Meta:
        model = Author
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']


class AuthorChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Author
        fields = ('username', 'email', 'first_name', 'last_name')


class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('bio', 'birth_date', 'location',)
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'short_description', 'full_description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'full_description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'short_description', 'full_description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'full_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }


class UnPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'is_published']
