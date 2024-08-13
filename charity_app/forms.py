from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm

class UserUpdateForm(UserChangeForm):

    password = forms.CharField(label ='Potwierdź hasło', widget=forms.PasswordInput)

    class Meta:
            model = User
            fields = ['username', 'first_name', 'last_name', 'email']
            help_texts = {
            'username': None,  # Usuwa domyślny help_text
        }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError('Nieprawidłowe hasło')
        return password