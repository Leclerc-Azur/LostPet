
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import logout
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import MyUser, OTP
from .forms import UserRegistrationForm, OTPVerifyForm
import random
from django.utils import timezone
from datetime import timedelta
from .forms import UserRegistrationForm, OTPVerifyForm, LoginForm
from .forms import ProfileSettingsForm


from .models import MyUser
from .forms import UserRegistrationForm

class RegisterView(CreateView):
    model = MyUser
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')  # после регистрации отправляем на логин

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_2fa_enabled:
                    code = f'{random.randint(100000, 999999)}'
                    OTP.objects.create(user=user, code=code)
                    send_mail(
                        'Код подтверждения входа',
                        f'Ваш код: {code}',
                        None,
                        [user.email],
                    )
                    request.session['2fa_user_id'] = user.id
                    return redirect('users:otp_verify')
                else:
                    login(request, user)
                    return redirect('users:profile')
            else:
                form.add_error(None, 'Неверный email или пароль.')
    return render(request, 'users/login.html', {'form': form})

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

    def form_valid(self, form):
        response = super().form_valid(form)
        # Вот обработка чекбокса:
        is_2fa = self.request.POST.get('is_2fa_enabled') == 'on'
        user = self.request.user
        user.is_2fa_enabled = is_2fa
        user.save()
        return response

    def get_object(self):
        return self.request.user

def otp_verify_view(request):
    user_id = request.session.get('2fa_user_id')
    if not user_id:
        return redirect('users:login')
    user = MyUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            # --- Время жизни кода 5 минут ---
            valid_time = timezone.now() - timedelta(minutes=5)
            otp_qs = OTP.objects.filter(user=user, code=code, created_at__gte=valid_time)
            if otp_qs.exists():
                login(request, user)
                otp_qs.delete()
                del request.session['2fa_user_id']
                return redirect('users:profile')
            else:
                form.add_error('code', 'Неверный или просроченный код')
    else:
        form = OTPVerifyForm()
    return render(request, 'users/otp_verify.html', {'form': form, 'email': user.email})