from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model, login

from .forms import NewUser
from data.models import Polygon

User = get_user_model()

class SignUp(generic.CreateView):
    form_class = NewUser
    success_url = reverse_lazy('home')
    template_name = 'account/signup.html'

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)

        return valid

class UserDetail(generic.DetailView, generic.list.MultipleObjectMixin):
    model = User
    template_name = 'account/user_detail.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        object_list = self.object.polygon.all()
        context = super(UserDetail, self).get_context_data(object_list=object_list, **kwargs)
        return context
    


class UserList(generic.ListView):
    model = User
    template_name = 'account/user_list.html'
    paginate_by = 20



def check_payment(request):
    for user in User.objects.all():
        user.profile.check_paid()

    return redirect('account:all')


    
