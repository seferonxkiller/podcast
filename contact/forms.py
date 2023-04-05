from django import forms
from .models import Contact, Sub


class SubForm(forms.ModelForm):
    class Meta:
        model = Sub
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'newsletter_input', 'placeholder': 'Email'
        })


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'id': 'name',
            'placeholder': 'name'
        })
        self.fields['message'].widget.attrs.update({
            'class': 'form-control',
            'id': 'message',
            'placeholder': 'message'
        })



