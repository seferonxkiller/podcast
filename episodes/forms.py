from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['author', 'article']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            "class": "comment_input",
            "placeholder": "Name"

        })

        self.fields['content'].widget.attrs.update({
            "class": "comment_input comment_textarea",
            'placeholder': 'Message',
            "cols": 30,
            "id": "message"
        })
