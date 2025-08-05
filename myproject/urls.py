from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),                         # регистрации/логин
    path('', include('lost_pets.urls', namespace='lost_pets')),      # главная — список потерянных питомцев
]

# В режиме DEBUG раздаём медиафайлы
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)