from django.urls import path, reverse_lazy
from .views import (
    RegisterView, login_view, LogoutView,
    ProfileView, ProfileSettingsView, otp_verify_view
)
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),  # кастомный логин с 2FA
    path('logout/', LogoutView.as_view(), name='logout'),

    # двухфакторка
    path('otp-verify/', otp_verify_view, name='otp_verify'),

    # --- Личный кабинет пользователя
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/settings/', ProfileSettingsView.as_view(), name='profile_settings'),

    # --- Смена пароля
    path(
        'profile/password/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html',
            success_url=reverse_lazy('users:password_change_done')
        ),
        name='password_change'
    ),
    path(
        'profile/password/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done'
    ),
]