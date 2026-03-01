from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *


# Форма отзыва
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш отзыв'
            })
        }
