from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from userprofile.models import Buyer


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nombre',
            'autocomplete': 'off'
        }))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Telefono',
            'autocomplete': 'off',
            # 'type': 'number'
        }
    ))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Correo',
            'autocomplete': 'off'
        }
    ))
    message = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Mensaje ',
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


class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Contraseña anterior',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Nueva contraseña',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirmar contraseña',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(label='Número de Teléfono', widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=15, required=False)
    address = forms.CharField(label='Dirección', widget=forms.Textarea(attrs={'class': 'form-control'}), max_length=250, required=False)
    full_name = forms.CharField(label="nombre completo", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=150, required=False)
    national_id = forms.CharField(label="Documento" , widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=20, required=False)
    # public_email = forms.CharField(widget=forms.EmailInput(attrs={ 'class': 'form-control' }), max_length=254, required=False)
    # url = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=50, required=False)
    # institution = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=50, required=False)
    # location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50, required=False)

    class Meta:
        model = Buyer
        fields = ['full_name', 'national_id', 'phone_number', 'address']