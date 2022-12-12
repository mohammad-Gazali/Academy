from django import forms
from django.utils.translation import gettext as _
from ckeditor.widgets import CKEditorWidget
from .models import Comment


attrs = {"class": "form-control"}

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {
            "content": _("Content")
        }
        widgets = {
            "content": forms.Textarea(attrs=attrs)
        }