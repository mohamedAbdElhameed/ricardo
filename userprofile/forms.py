from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'name',
            'autocomplete': 'off'
        }))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'phono',
            'autocomplete': 'off',
            # 'type': 'number'
        }
    ))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'email',
            'autocomplete': 'off'
        }
    ))
    message = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'message',
            'autocomplete': 'off'
        }
    ))
