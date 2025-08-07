from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),


    path('accounts/', include(('users.urls', 'users'), namespace='users')),

    path('', include(('lost_pets.urls', 'lost_pets'), namespace='lost_pets')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATICFILES_DIRS[0],
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )