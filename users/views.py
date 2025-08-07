from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import logout
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import ProfileSettingsForm


from .models import MyUser
from .forms import UserRegistrationForm

class RegisterView(CreateView):
    model = MyUser
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')  # после регистрации отправляем на логин

class LoginView(AuthLoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class LogoutView(AuthLogoutView):
    # куда редиректить после logout
    next_page = reverse_lazy('lost_pets:index')
    # позволяем и GET, и POST
    http_method_names = ['get', 'post', 'head', 'options']

    def get(self, request, *args, **kwargs):
        # явно выходим
        logout(request)
        return redirect(self.next_page)

    def post(self, request, *args, **kwargs):
        # для надёжности POST → тот же get()
        return self.get(request, *args, **kwargs)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

class ProfileSettingsView(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = ProfileSettingsForm
    template_name = 'users/profile_settings.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user



