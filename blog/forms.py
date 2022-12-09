from django.utils.translation import gettext as _
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Article


attrs = {'class': 'form-control'}


class ArticleForm(forms.ModelForm):

    class Meta:
        
        model = Article
        
        fields = ['title', 'category', 'body', 'is_arabic']
        
        labels = {
            'title': _("Title"),
            'category': _("Category"),
            'body': _("Body"),
            'is_arabic': _("Is The Article Written in Arabic ?"),
        }
        
        widgets = {
            'title': forms.TextInput(attrs=attrs),
            'category': forms.Select(attrs=attrs),
            'body': CKEditorWidget(),
            'is_arabic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }