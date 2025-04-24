from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

# forms.py
from django import forms
from .models import Subscriber

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'your-email-input-class',
                'placeholder': 'Enter your email'
            }),
            'name': forms.TextInput(attrs={
                'class': 'your-name-input-class',
                'placeholder': 'Your name (optional)'
            })
        }