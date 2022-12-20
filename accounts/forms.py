from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django import forms

attrs = {'class': 'form-control'}


class UserLoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs=attrs)
    )

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs=attrs)
    )

    class Meta:
        labels = {
            "username": _('Username'),
            "password": _('Password')
        }



class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label=_('First Name'),
        widget= forms.TextInput(attrs=attrs)
    )

    last_name = forms.CharField(
        label=_('Last Name'),
        widget= forms.TextInput(attrs=attrs)
    )

    username = forms.CharField(
        label=_('Username'),
        widget= forms.TextInput(attrs=attrs)
    )

    email = forms.EmailField(
        label=_('Email'),
        widget= forms.TextInput(attrs=attrs)
    )

    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs=attrs)
    )
    
    password2 = forms.CharField(
        label=_('Password Confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs=attrs)
    )

    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'last_name', 'username', 'email')
        labels = {
            "first_name": _('First Name'),
            "last_name": _('Last Name'),
            "username": _('Username'),
            "email": _('Email'),
            "password1": _('Password'),
            "password2": _('Password Confirmation')
        }