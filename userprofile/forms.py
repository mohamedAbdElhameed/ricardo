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


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'class': 'input',
            'id': 'user',
            'type': 'text',
            'autocomplete': 'off'

        }
    ))

    password = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'class': 'input',
            'id': 'pass',
            'type': 'password',
            'data-type': 'password',
            'autocomplete': 'off'
        }
    ))

    re_password = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'class': 'input',
            'id': 'pass',
            'type': 'password',
            'data-type': 'password',
            'autocomplete': 'off'
        }
    ))

    email = forms.EmailField(max_length=50, widget=forms.EmailInput(
        attrs={
            'class': 'input',
            'id': 'email',
            'type': 'email',
            'autocomplete': 'off'
        }
    ))


class LoginForm(forms.Form):
    username = username = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'class': 'input',
            'id': 'user',
            'type': 'text',
            'autocomplete': 'off'

        }
    ))

    password = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'class': 'input',
            'id': 'pass',
            'type': 'password',
            'data-type': 'password',
            'autocomplete': 'off'
        }
    ))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

