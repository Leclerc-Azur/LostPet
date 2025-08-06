from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from .models import MyUser
from .forms import UserRegistrationForm

class RegisterView(CreateView):
    model = MyUser
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:two_factor_settings')

class LoginView(AuthLoginView):
    template_name = 'users/two_factor_settings.html'

class LogoutView(AuthLogoutView):
    next_page = reverse_lazy('users:two_factor_settings')