from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import LostAnimal
from .forms import LostAnimalForm

class LostAnimalListView(ListView):
    """Список всех активных объявлений о пропавших животных."""
    model = LostAnimal
    template_name = 'lost_pets/index.html'        # <-- указываем ваш index.html
    context_object_name = 'animals'
    paginate_by = 10

    def get_queryset(self):
        # только активные, сортируем по дате создания
        return super().get_queryset().filter(is_active=True).order_by('-created_at')


class LostAnimalDetailView(DetailView):
    """Детальная страница объявления."""
    model = LostAnimal
    template_name = 'lost_pets/lostanimal_detail.html'
    context_object_name = 'animal'


class LostAnimalCreateView(LoginRequiredMixin, CreateView):
    """Форма создания объявления — только для залогиненных."""
    model = LostAnimal
    form_class = LostAnimalForm
    template_name = 'lost_pets/lostanimal_form.html'
    success_url = reverse_lazy('lost_pets:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)