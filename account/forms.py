from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class NewUser(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')