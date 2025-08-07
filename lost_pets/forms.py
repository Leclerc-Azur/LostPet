from django import forms
from .models import LostAnimal, City, District

class LostAnimalForm(forms.ModelForm):
    area = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label='Область',
        empty_label='— выберите область —'
    )
    city = forms.ModelChoiceField(
        queryset=District.objects.none(),
        label='Город',
        empty_label='— выберите город —'
    )

    class Meta:
        model = LostAnimal
        fields = [
            'title', 'category', 'phone', 'description',
            'cover', 'address', 'date_lost', 'gender'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            # Вот тут мы указываем HTML5 date-picker
            'date_lost': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'дд.мм.гггг'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'area' in self.data:
            try:
                area_id = int(self.data.get('area'))
                self.fields['city'].queryset = District.objects.filter(city_id=area_id)
            except (ValueError, TypeError):
                self.fields['city'].queryset = District.objects.none()
        elif self.instance.pk and self.instance.city:
            self.fields['city'].queryset = District.objects.filter(city=self.instance.city)
            self.fields['area'].initial = self.instance.city

    def clean(self):
        cleaned_data = super().clean()
        area = cleaned_data.get('area')
        city = cleaned_data.get('city')
        if area and city and city.city != area:
            self.add_error('city', 'Город не принадлежит выбранной области.')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.city = self.cleaned_data.get('area')
        instance.district = self.cleaned_data.get('city')
        if commit:
            instance.save()
            self.save_m2m()
        return instance