from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser, OTP

@admin.register(MyUser)
class MyUserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'username', 'role', 'is_admin', 'is_active')
    list_filter  = ('role', 'is_admin', 'is_active')
    search_fields = ('email', 'username')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональные данные', {'fields': ('username', 'avatar')}),
        ('Права доступа', {'fields': ('role', 'is_active', 'is_admin', 'is_2fa_enabled')}),
        ('Важные даты', {'fields': ('last_login', 'created_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )

    # Здесь обязательно нужно задать пустой кортеж:
    filter_horizontal = ()

admin.site.register(OTP)