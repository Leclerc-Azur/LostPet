from django.utils.translation import gettext_lazy as _

class UserRoleChoices:
    MANAGER = 'manager'
    STANDARD_USER = 'user'

    CHOICES = [
        (MANAGER, _('Менеджер')),
        (STANDARD_USER, _('Пользователь')),
    ]