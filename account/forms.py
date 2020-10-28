from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class NewUser(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password')
        model = get_user_model()