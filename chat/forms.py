from django.forms import ValidationError
from django.contrib.auth.models import User
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "id": "login-username"}
        ),
    )
    password = forms.CharField(
        label="Password",
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "id": "login-password"}
        ),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "id": "register-username"}
        ),
    )
    first_name = forms.CharField(
        label="Firstname",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Firstname"}),
    )
    last_name = forms.CharField(
        label="Lastname",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Lastname"}),
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Email"}),
    )
    password = forms.CharField(
        label="Password",
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "id": "register-password"}
        ),
    )

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["email"],
            last_name=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )

        return user
