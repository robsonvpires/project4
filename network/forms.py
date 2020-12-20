from django import forms

class NewPostForm(forms.Form):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'what is going on now?'
    })) 