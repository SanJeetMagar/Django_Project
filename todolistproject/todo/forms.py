from django import forms
from .models import Todo
from django.contrib.auth.models import User

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter todo title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description (optional)'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        widgets = {
            "username": forms.TextInput(attrs = {"class": "form-control"}),
            "password": forms.TextInput(attrs= {"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        help_texts = {
            "username": None,
            "password" : None,
            "email": None,
        }