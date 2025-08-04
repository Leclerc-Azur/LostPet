from django.contrib import admin
from .models import LostAnimal

class CityFilter(admin.SimpleListFilter):
    """Фильтр для админки по городу."""
    title = 'город'
    parameter_name = 'city'

    def lookups(self, request, model_admin):
        return [(city.id, city.title) for city in model_admin.model.city.field.related_model.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(city_id=self.value())
        return queryset