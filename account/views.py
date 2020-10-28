from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import NewUser

class SignUp(CreateView):
    form_class = NewUser
    success_url = reverse_lazy('login')
    template_name = 'account/signup.html'
    
