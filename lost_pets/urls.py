from django.urls import path
from .views import LostAnimalListView, LostAnimalDetailView, LostAnimalCreateView

app_name = 'lost_pets'
urlpatterns = [
    path('',        LostAnimalListView.as_view(),   name='list'),
    path('create/', LostAnimalCreateView.as_view(), name='create'),
    path('<int:pk>/', LostAnimalDetailView.as_view(), name='detail'),
]