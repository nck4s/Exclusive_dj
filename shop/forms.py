from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'auth-input',
            'placeholder': 'Email or Phone Number'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'auth-input',
            'placeholder': 'Password'
        })
    )


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']  # только нужные поля
        help_texts = {
            'username': None,
            'password1': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        if 'password2' in self.fields:
            del self.fields['password2']


        self.fields['username'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Name',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Password',
        })

