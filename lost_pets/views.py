from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.http import JsonResponse
from django.views import View
from .models import LostAnimal, City, District
from .forms import LostAnimalForm
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.views.generic import TemplateView



class LostAnimalListView(ListView):
    model = LostAnimal
    template_name = 'lost_pets/index.html'
    context_object_name = 'animals'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by('-created_at')

class LostAnimalSearchView(ListView):
    model = LostAnimal
    template_name = 'lost_pets/search.html'
    context_object_name = 'animals'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True).order_by('-created_at')
        area = self.request.GET.get('area')
        city = self.request.GET.get('city')
        if area:
            qs = qs.filter(city_id=area)
        if city:
            qs = qs.filter(district_id=city)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['areas']  = City.objects.all().order_by('title')
        area = self.request.GET.get('area')
        ctx['cities'] = (
            District.objects.filter(city_id=area).order_by('title')
            if area else District.objects.none()
        )
        ctx['selected_area']  = area or ''
        ctx['selected_city'] = self.request.GET.get('city') or ''
        return ctx

class LostAnimalDetailView(DetailView):
    model = LostAnimal
    template_name = 'lost_pets/lostanimal_detail.html'
    context_object_name = 'animal'

class LostAnimalCreateView(LoginRequiredMixin, CreateView):
    model = LostAnimal
    form_class = LostAnimalForm
    template_name = 'lost_pets/lostanimal_form.html'
    success_url = reverse_lazy('lost_pets:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Объявление успешно опубликовано!")
        return super().form_valid(form)

class LoadCitiesView(View):
    def get(self, request):
        area_id = request.GET.get('area_id')
        data = []
        if area_id:
            qs = District.objects.filter(city_id=area_id).order_by('title')
            data = [{'id': d.pk, 'name': d.title} for d in qs]
        return JsonResponse({'cities': data})

class UserIsAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        user = self.request.user

        # Если менеджер — разрешить удалять всё
        if hasattr(user, "role") and user.role == "manager":
            return True
        # Иначе только автор
        return obj.user == user

class LostAnimalUpdateView(LoginRequiredMixin, UserIsAuthorMixin, UpdateView):
    model = LostAnimal
    form_class = LostAnimalForm
    template_name = 'lost_pets/lostanimal_form.html'   # Тот же шаблон, что и для создания
    success_url = reverse_lazy('lost_pets:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LostAnimalDeleteView(LoginRequiredMixin, UserIsAuthorMixin, DeleteView):
    model = LostAnimal
    template_name = 'lost_pets/lostanimal_confirm_delete.html'  # Нужно создать этот шаблон
    success_url = reverse_lazy('lost_pets:index')


class MyAdsListView(LoginRequiredMixin, ListView):
    model = LostAnimal
    template_name = 'users/profile.html'
    context_object_name = 'my_animals'

    def get_queryset(self):
        # Возвращаем только объявления этого пользователя
        return LostAnimal.objects.filter(user=self.request.user).order_by('-created_at')

def donate_view(request):
    if request.method == 'POST':
        messages.success(request, 'Спасибо за ваше пожертвование!')
        return redirect('lost_pets:index')  # или 'home' — на что указывает твоя главная
    return render(request, 'lost_pets/donate.html')

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['user_ads'] = LostAnimal.objects.filter(user=user)
        return context