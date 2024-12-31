from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class RegisterModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Parol")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={'class': 'login-input', 'placeholder': 'E-pochta'})
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={'class': 'login-input', 'placeholder': 'Parol'})
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
            return self.cleaned_data
