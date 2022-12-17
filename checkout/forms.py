from django import forms
from django.utils.translation import gettext as _


class UserInfoForm(forms.Form):
    first_name = forms.CharField(max_length=255, label=_("first name"))
    last_name = forms.CharField(max_length=255, label=_("last name"))
    email = forms.EmailField(label=_("email"))