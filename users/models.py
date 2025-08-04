from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    """Возможные роли пользователя."""
    MANAGER = 'manager', _('Менеджер')
    STANDARD_USER = 'user', _('Пользователь')

class MyUserManager(BaseUserManager):
    """Менеджер для работы с пользовательской моделью."""
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Создание суперпользователя (администратора)."""
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('role', UserRole.MANAGER)
        return self.create_user(username, email, password, **extra_fields)

class MyUser(AbstractBaseUser):
    """Кастомная модель пользователя."""
    username = models.CharField(max_length=222, verbose_name='Имя пользователя')
    email = models.EmailField(unique=True, verbose_name='Адрес электронной почты')
    avatar = models.ImageField(
        upload_to='media/user_avatars',
        blank=True,
        null=True,
        verbose_name='Аватарка'
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STANDARD_USER,
        verbose_name='Роль'
    )
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_2fa_enabled = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Простейшая проверка наличия прав."""
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        """Админ может входить в админ‑панель."""
        return self.is_admin

class OTP(models.Model):
    """Одноразовый пароль для двухфакторной аутентификации."""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)