from django import forms

from .models import User


class CustomUserCreationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder': 'name@example.com'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'id': 'floatingPassword',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'id': 'floatingPassword2',
            'placeholder': 'Password'
        })
    )

    def password_validation(self):
        data = self.cleaned_data
        if data['password1'] == data['password2']:
            return True
        return False


class LoginUserForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'class': 'form-control rounded-3',
            'id': 'floatingInput',
            'placeholder': 'name@example.com'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control rounded-3',
            'id': 'floatingPassword',
            'placeholder': 'Password'

        })
    )


class OtpForm(forms.Form):
    otp = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'text',
            'class': 'form-control rounded-3',
            'id': 'floatingInput'
        })
    )