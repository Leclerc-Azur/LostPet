from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import LostAnimal
from .forms import LostAnimalForm

class LostAnimalListView(ListView):
    """Список всех объявлений о пропавших животных."""
    model = LostAnimal
    template_name = 'lost_pets/lostanimal_list.html'
    context_object_name = 'animals'
    paginate_by = 10   # по 10 объявлений на страницу

    def get_queryset(self):
        # только активные объявления
        return super().get_queryset().filter(is_active=True).order_by('-created_at')

class LostAnimalDetailView(DetailView):
    """Детальная страница объявления."""
    model = LostAnimal
    template_name = 'lost_pets/lostanimal_detail.html'
    context_object_name = 'animal'

class LostAnimalCreateView(LoginRequiredMixin, CreateView):
    """Форма создания объявления — доступна только для залогиненных."""
    model = LostAnimal
    form_class = LostAnimalForm
    template_name = 'lost_pets/lostanimal_form.html'
    success_url = reverse_lazy('lost_pets:list')

    def form_valid(self, form):
        # присвоим авторство текущему пользователю
        form.instance.user = self.request.user
        return super().form_valid(form)