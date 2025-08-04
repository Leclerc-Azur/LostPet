from django.contrib import admin
from .models import City, District, AnimalCategory, LostAnimal, LostAnimalImage

class LostAnimalImageInline(admin.TabularInline):
    model = LostAnimalImage
    extra = 1  # Позволяет добавлять несколько фото в объявлении

@admin.register(LostAnimal)
class LostAnimalAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'city', 'district', 'created_at', 'is_active')
    list_filter = ('category', 'city', 'district', 'is_active')
    search_fields = ('title', 'description', 'phone')
    inlines = [LostAnimalImageInline]

admin.site.register(City)
admin.site.register(District)
admin.site.register(AnimalCategory)