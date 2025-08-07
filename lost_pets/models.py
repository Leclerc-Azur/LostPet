from django.db import models
from django.contrib.auth import get_user_model

GENDER_CHOICES = [
    ('male', 'Самец'),
    ('female', 'Самка'),
    ('unknown', 'Неизвестно'),
]

User = get_user_model()

class City(models.Model):
    """Область, в которой пропало животное."""
    title = models.CharField(max_length=255, verbose_name='Область')

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'

    def __str__(self):
        return self.title

class District(models.Model):
    """Город (раньше район) в указанной области."""
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name='districts',
        verbose_name='Область'
    )
    title = models.CharField(max_length=255, verbose_name='Город')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return f'{self.city}: {self.title}'

class AnimalCategory(models.Model):
    """Категория животного (например, кошка, собака)."""
    title = models.CharField(max_length=100, verbose_name='Категория')
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name='Родительская категория'
    )

    class Meta:
        verbose_name = 'Категория животного'
        verbose_name_plural = 'Категории животных'

    def __str__(self):
        names = [self.title]
        parent = self.parent_category
        while parent:
            names.append(parent.title)
            parent = parent.parent_category
        return ' > '.join(reversed(names))

class LostAnimal(models.Model):
    """Объявление о пропавшем животном."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lost_animals',
        verbose_name='Автор'
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    category = models.ForeignKey(
        AnimalCategory,
        on_delete=models.PROTECT,
        related_name='lost_animals',
        verbose_name='Категория животного'
    )
    phone = models.CharField(max_length=30, verbose_name='Телефон для связи')
    description = models.TextField(verbose_name='Описание')
    cover = models.ImageField(
        upload_to='media/lost_animals/covers',
        blank=True,
        null=True,
        verbose_name='Обложка'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name='lost_animals',
        verbose_name='Область'
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name='lost_animals',
        verbose_name='Город'
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Адрес/ориентир'
    )
    date_lost = models.DateField(verbose_name='Дата пропажи', null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='unknown',
        verbose_name='Пол'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Пропавшее животное'
        verbose_name_plural = 'Пропавшие животные'

    def __str__(self):
        return f'{self.title} ({self.category})'

class LostAnimalImage(models.Model):
    """Дополнительные фотографии для объявления."""
    lost_animal = models.ForeignKey(
        LostAnimal,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Объявление'
    )
    image = models.ImageField(
        upload_to='media/lost_animals/images',
        verbose_name='Фотография'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Фотография пропавшего животного'
        verbose_name_plural = 'Фотографии пропавших животных'

    def __str__(self):
        return f'Фото для {self.lost_animal.title}'