from django.urls import path, reverse_lazy
from .views import (
    RegisterView, LoginView, LogoutView,
    ProfileView, ProfileSettingsView
)
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    # --- Регистрация, вход, выход
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',    LoginView.as_view(),    name='login'),
    path('logout/',   LogoutView.as_view(),   name='logout'),

    # --- Личный кабинет пользователя
    path('profile/',            ProfileView.as_view(),           name='profile'),
    path('profile/settings/',   ProfileSettingsView.as_view(),   name='profile_settings'),

    # --- Смена пароля
    path(
        'profile/password/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html',
            success_url=reverse_lazy('users:password_change_done')  # это обязательно!
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