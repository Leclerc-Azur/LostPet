from django.urls import path
from .views import (
    LostAnimalListView,
    LostAnimalSearchView,
    LostAnimalCreateView,
    LostAnimalDetailView,
    LoadCitiesView,

)
from .views import LostAnimalUpdateView, LostAnimalDeleteView
from . import views
from .views import donate_view

app_name = 'lost_pets'

urlpatterns = [
    # главная — все объявления
    path('', LostAnimalListView.as_view(), name='index'),

    # поиск — фильтрация по области/городу
    path('search/', LostAnimalSearchView.as_view(), name='search'),

    # создать своё объявление
    path('create/', LostAnimalCreateView.as_view(), name='create'),

    # детальный просмотр
    path('<int:pk>/', LostAnimalDetailView.as_view(), name='detail'),

    # AJAX для подгрузки городов
    path('ajax/load-cities/', LoadCitiesView.as_view(), name='ajax_load_cities'),
    path('edit/<int:pk>/', LostAnimalUpdateView.as_view(), name='lostanimal_edit'),
    path('delete/<int:pk>/', LostAnimalDeleteView.as_view(), name='lostanimal_delete'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('donate/', donate_view, name='donate'),
]