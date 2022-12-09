from django.views.generic import CreateView
from django.urls import reverse
from django.contrib.auth import login
from .forms import UserRegisterForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration/register.html'

    def get_success_url(self):
        login(self.request, self.object)
        return reverse('home')