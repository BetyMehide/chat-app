from django import forms

from .models import ConversationModel


class ConversationCreateForm(forms.ModelForm):
    class Meta:
        model = ConversationModel
        fields = ["title", "description", "date"]
