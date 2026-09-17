from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class RegisterForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('supplier', 'Supplier'),
        ('staff', 'Staff'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="Register as"
    )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role')

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        label="Password",
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label="Confirm Password",
    )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name',
            'email',
            'phone_number',
            'address',
            'company',
            'profile_picture',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

