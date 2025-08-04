from django.utils.translation import gettext_lazy as _

class LostAnimalStatus:
    ACTIVE = 'active'
    CLOSED = 'closed'
    CHOICES = [
        (ACTIVE, _('Активно')),
        (CLOSED, _('Закрыто')),
    ]